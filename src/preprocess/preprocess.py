import numpy as np
import pyvista as pv
from pathlib import Path
from pyNastran.bdf.bdf import BDF
from pyNastran.op2.op2 import OP2
from pyNastran.op4.op4 import OP4
from src.utils import utils, dat


#phi = np.column_stack(mode_shapes)

# this is a class so i can access the data inside

class preprocess:
    def __init__(self, program_input):
        self.program_input = program_input

        

        self.read_nastran()

        self.openfoam_cases = {}
        for freestream_vel, path in program_input.openfoam_files.items():
            self.openfoam_cases[freestream_vel] = self.read_openfoam()



### NASTRAN 
    def read_nastran(self):
        ## I/O
        if not Path(self.program_input.nastran_bdf_path).exists():
            raise FileNotFoundError(f"Input BDF file not found: {self.program_input.nastran_bdf_path}")
        bdf_path = self.program_input.nastran_bdf_path

        if not Path(self.program_input.nastran_op2_path).exists():
            raise FileNotFoundError(f"Input op2 file not found: {self.program_input.nastran_op2_path}")
        op2_path = self.program_input.nastran_op2_path

        if not Path(self.program_input.nastran_op4_path).exists():
            raise FileNotFoundError(f"Input op4 file not found: {self.program_input.nastran_op4_path}")
        op4_path = self.program_input.nastran_op4_path


        ## Read
        with utils.runtime("read bdf"):       # FEM
            self.model = BDF()
            self.model.read_bdf(bdf_path)
            
        with utils.runtime("read op2"):       # mode shapes and eigenvectors
            self.results = OP2()
            self.results.read_op2(op2_path) #, build_dataframe=True)

            modes = self.results.eigenvectors  # dict: {subcase_id: EigenvectorObject}

            # Get first subcase mode shapes matrix (modes for each DOF and mode)
            first_subcase_id = list(modes.keys())[0]
            mode_obj = modes[first_subcase_id]

            # mode_obj.vectors is a numpy array of mode shapes:
            # shape = (number_of_DOFs, number_of_modes)
            self.phi = mode_obj.vectors

            
        with utils.runtime("read op4"):       # global matrices
            op4 = OP4()
            self.k_stiff = utils.trans_matrix_phys_to_modal( self.phi, op4.read_op4(op4_path, matrix_names=['KGG']) )
            self.m_mass = utils.trans_matrix_phys_to_modal( self.phi,op4.read_op4(op4_path, matrix_names=['MGG']) )


### OpenFOAM
    def read_openfoam(self):

        ## I/O
        if not Path(self.program_input.openfoam_cfd_path).exists():
            raise FileNotFoundError(f"Input OpenFoam CFD file not found: {self.program_input.openfoam_cfd_path}")
        self.cfd_path = self.program_input.openfoam_cfd_path

        # Load mesh and field data
        mesh = pv.read(self.program_input.openfoam_cfd_path)

        # Extract fields
        pressures = mesh.point_data.get('p')           # Pressure
        densities = mesh.point_data.get('rho')          # Density
        velocities = mesh.point_data.get('U')           # Velocity vector
        speeds_of_sound = mesh.point_data.get('a')     # Speed of sound

        return dat.OpenFOAMcase(
            pressures=pressures,
            densities=densities,
            speeds_of_sound=speeds_of_sound,
            velocities=velocities
        )

    def get_freestream_speeds(self):
        return list(self.openfoam_cases.keys())

    def build_node_plus_dict(self):

        node_ids = sorted(self.model.nodes.keys())
        coords = np.array([self.model.nodes[nid].xyz for nid in node_ids])

        # Build list of node_plus instances
        nodes = {}
        for i, nid in enumerate(node_ids):
            nodes[nid] = dat.node_plus(
                r_=coords[nid],
                p=float(pressure[i]),
                rho=float(density[i]),
                a=float(speed_of_sound[i]),
                u_= velocity[i],
                F_aero_=np.array([0.0, 0.0, 0.0])
            )

        return nodes

    def build_cquad4_panel_array(self, nodes):
        panels = []

        for eid, elem in self.model.elements.items():
            if elem.type == 'CQUAD4':
                panel = dat.cquad4_panel(elem, nodes)
                panels.append(panel)

