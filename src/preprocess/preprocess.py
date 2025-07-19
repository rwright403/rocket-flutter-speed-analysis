import numpy as np
from pathlib import Path
import os
import importlib
from pyNastran.bdf.bdf import BDF
from pyNastran.op2.op2 import OP2
from src.utils import utils, dat


### NASTRAN 
def read_nastran(input_module, self):
    program_input = importlib.import_module(f"src.inputs.{input_module}")
    
    ## I/O
    if not Path(program_input.nastran_bdf_path).exists():
        raise FileNotFoundError(f"Input BDF file not found: {program_input.nastran_bdf_path}")
    bdf_path = program_input.nastran_bdf_path

    if not Path(program_input.nastran_op2_path).exists():
        raise FileNotFoundError(f"Input op2 file not found: {program_input.nastran_op2_path}")
    op2_path = program_input.nastran_op2_path

    if not Path(program_input.nastran_mat_path).exists():
        raise FileNotFoundError(f"Input mat file not found: {program_input.nastran_mat_path}")
    full_mat_path = program_input.nastran_mat_path



    ## Read
    with utils.runtime("read .bdf"):       # FEM
        model = BDF()
        model.read_bdf(bdf_path)
        
    with utils.runtime("read .op2"):       # mode shapes and eigenvectors
        results = OP2()
        results.read_op2(op2_path)

        modes = results.eigenvectors  # dict: {subcase_id: EigenvectorObject}

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

        phi = np.column_stack(phi_list)  # shape: (n_dofs, n_modes)
        #print("phi shape:", self.phi.shape)

        
    with utils.runtime("read .mat"):       # global matrices
        KGG = utils.read_and_parse_full_matrix("STIFFNESS", full_mat_path)
        MGG = utils.read_and_parse_full_matrix("MASS", full_mat_path)
        DOFS = utils.read_and_parse_full_matrix("DOFS", full_mat_path)

    return dat.NASTRANsol103(
        model,
        results,
        phi,
        KGG,
        MGG,
        DOFS,
    )

### OpenFOAM
def read_openfoam_case(path):
    ## I/O
    path = Path(path).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"Input OpenFoam CFD postProcessing not found: {path}")


    # Extract fields
    pressures = utils.read_last_probe_column(os.path.expanduser(os.path.join(path, 'p')))         # Pressure
    densities = utils.read_last_probe_column(os.path.expanduser(os.path.join(path, 'rho')))           # Density
    velocities = utils.read_last_probe_column(os.path.expanduser(os.path.join(path, 'U')))           # Velocity vector
    temperatures = utils.read_last_probe_column(os.path.expanduser(os.path.join(path, 'T')))        # Temperature - used to sol Speed of sound

    return dat.OpenFOAMcase(
        pressures=pressures,
        densities=densities,
        temperatures=temperatures,
        velocities=velocities
    )

def read_openfoam(input_module):
    program_input = importlib.import_module(f"src.inputs.{input_module}")
    openfoam_cases = {}

    for freestream_vel, path in program_input.openfoam_files.items():
        #print("path: ", path)
        openfoam_cases[freestream_vel] = read_openfoam_case(path)

    return openfoam_cases

