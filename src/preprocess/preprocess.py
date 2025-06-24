import numpy as np
import pyvista as pv
from pathlib import Path
import importlib
from pyNastran.bdf.bdf import BDF
from pyNastran.op2.op2 import OP2
from src.utils import utils, dat


#phi = np.column_stack(mode_shapes)

# this is a class so i can access the data inside

class preprocess:
    def __init__(self, input_file):

        # Dynamically import the input file
        self.program_input = importlib.import_module(f"src.inputs.{input_file}")

        self.model = None
        self.results = None
        self.phi = None
        self.KGG = None
        self.MGG = None

        self.read_nastran()

        
        self.openfoam_cases = {}

        for freestream_vel, path in self.program_input.openfoam_files.items():
            self.openfoam_cases[freestream_vel] = self.read_openfoam(path)

        self.freestream_speeds = self.get_freestream_speeds()
        



### NASTRAN 
    def read_nastran(self):
        ## I/O
        if not Path(self.program_input.nastran_bdf_path).exists():
            raise FileNotFoundError(f"Input BDF file not found: {self.program_input.nastran_bdf_path}")
        bdf_path = self.program_input.nastran_bdf_path

        if not Path(self.program_input.nastran_op2_path).exists():
            raise FileNotFoundError(f"Input op2 file not found: {self.program_input.nastran_op2_path}")
        op2_path = self.program_input.nastran_op2_path

        if not Path(self.program_input.nastran_mat_path).exists():
            raise FileNotFoundError(f"Input mat file not found: {self.program_input.nastran_mat_path}")
        full_mat_path = self.program_input.nastran_mat_path


        ## Read
        with utils.runtime("read .bdf"):       # FEM
            self.model = BDF()
            self.model.read_bdf(bdf_path)
            
        with utils.runtime("read .op2"):       # mode shapes and eigenvectors
            self.results = OP2()
            self.results.read_op2(op2_path) #, build_dataframe=True)

            modes = self.results.eigenvectors  # dict: {subcase_id: EigenvectorObject}

            # Get first subcase mode shapes matrix (modes for each DOF and mode)
            first_subcase_id = list(modes.keys())[0]
            mode_obj = modes[first_subcase_id]

            print("Type of mode_obj:", type(mode_obj))

            # Each mode is stored separately, so we extract all displacement vectors
            n_modes, n_nodes, n_dofs_per_node = mode_obj.data.shape

            # Each mode's shape: (n_nodes * 6,) flattened displacement
            phi_list = [
                mode_obj.data[i_mode].reshape(-1)  # Flatten to (n_nodes*6,)
                for i_mode in range(n_modes)
            ]

            self.phi = np.column_stack(phi_list)  # shape: (n_dofs, n_modes)
            #print("phi shape:", self.phi.shape)


            
        with utils.runtime("read .mat"):       # global matrices
            self.KGG = utils.read_and_parse_mat_file("STIFFNESS",full_mat_path)
            self.MGG = utils.read_and_parse_mat_file("MASS",full_mat_path)
            

### OpenFOAM
    def read_openfoam(self, path):

        ## I/O
        if not Path(path).exists():
            raise FileNotFoundError(f"Input OpenFoam CFD file not found: {path}")

        # Load mesh and field data
        mesh = pv.read(path)

        # Extract fields
        pressures = mesh.point_data.get('p')           # Pressure
        densities = mesh.point_data.get('rho')          # Density
        velocities = mesh.point_data.get('U')           # Velocity vector
        speeds_of_sound = mesh.point_data.get('a')     # Speed of sound

        return dat.OpenFOAMcase(
            #NOTE: SEE NOTE ON PRESSURE REAL: 
            pressures=pressures, #TODO: THERE WOULD BE 2 PRESSURES,ON ON EACH SIDE OF PLANE SO SHOULD I SUBTRACT THEM HERE AND TAKE DIFFERENCE OF PRESSURE?
            densities=densities,
            speeds_of_sound=speeds_of_sound,
            velocities=velocities
        )

    def get_freestream_speeds(self):
        return list(self.openfoam_cases.keys())

    def build_node_plus_dict(self, cfd_case):

        node_ids = sorted(self.model.nodes.keys())
        coords = np.array([self.model.nodes[nid].xyz for nid in node_ids])

        nodes = {}
        # Build list of node_plus instances
        for i, nid in enumerate(node_ids):

            nodes[nid] = dat.node_plus(
                r_=coords[nid],
                p=(cfd_case.pressure[i]),
                rho=(cfd_case.density[i]),
                a=(cfd_case.speed_of_sound[i]),
                u_= cfd_case.velocity[i],
            )
        return nodes

    ### ???
    def build_cquad4_panel_array(self):
        panels = []

        for eid, elem in self.model.elements.items():
            if elem.type == 'CQUAD4':
                panel = dat.cquad4_panel(elem, nodes)
                panels.append(panel)

