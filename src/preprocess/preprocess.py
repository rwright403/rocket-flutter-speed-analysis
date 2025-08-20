import numpy as np
from pathlib import Path
import os
import importlib
from pyNastran.bdf.bdf import BDF
from pyNastran.op2.op2 import OP2
from src.utils import utils, dat
from io import StringIO
import pandas as pd


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

        n_dofs = n_nodes * n_dofs_per_node

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
        n_dofs,
    )

### OpenFOAM cfd

def read_openfoam_last_probe_column(filename):
    with open(filename, 'r') as f:
        # Read and filter non-comment lines
        data_lines = [line for line in f if not line.strip().startswith('#')]

    # Use pandas to parse the filtered lines
    df = pd.read_csv(
        StringIO(''.join(data_lines)),
        delim_whitespace=True, 
        header=None
    )

    # Return only the last column (one probe value per time)
    return df.iloc[:, -1]  # This is a Series

def read_openfoam_cfd_samplepts(path):
    ## I/O
    path = Path(path).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"Input OpenFOAM CFD postProcessing not found: {path}")

    temperatures = read_openfoam_last_probe_column(os.path.expanduser(os.path.join(path, 'T')))

    return dat.CFDsamplepts(
        pressures = read_openfoam_last_probe_column(os.path.expanduser(os.path.join(path, 'p'))),
        densities = read_openfoam_last_probe_column(os.path.expanduser(os.path.join(path, 'rho'))),
        speed_of_sounds = np.sqrt(dat.GAMMA * dat.R_SPEC_AIR * temperatures),
        velocities = read_openfoam_last_probe_column(os.path.expanduser(os.path.join(path, 'U')))
    )

### Ansys CFX cfd

def read_cfx_cfd_samplepts(path):
    ## I/O
    path = Path(path).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"Input CFX CFD postProcessing not found: {path}")

    # Read all lines
    with open(path, 'r') as f:
        lines = f.readlines()


# Find '[Data]' section and skip header line
    for i, line in enumerate(lines):
        if line.strip() == '[Data]':
            header_idx = i + 1
            data_start = i + 2
            break

    # Extract header row
    headers = [h.strip() for h in lines[header_idx].split(',')]

    df = pd.read_csv(path, skiprows=data_start, names=headers)

    # Extract fields as numpy arrays
    temperatures = df["Temperature [ K ]"].to_numpy()

    return dat.CFDsamplepts(
        pressures=df["Static Pressure [ Pa ]"].to_numpy(),
        densities=df["Density [ kg m^-3 ]"].to_numpy(),
        speed_of_sounds = np.sqrt(dat.GAMMA * dat.R_SPEC_AIR * temperatures),
        velocities = np.stack([ 
            df["Velocity u [ m s^-1 ]"].to_numpy(), 
            df["Velocity v [ m s^-1 ]"].to_numpy(), 
            df["Velocity w [ m s^-1 ]"].to_numpy() 
        ], axis=1)
    )



def read_cfd(input_module):
    program_input = importlib.import_module(f"src.inputs.{input_module}")
    cfd_cases = []

    samplepts: dat.CFDsamplepts

    for cfd_input in program_input.cfd_inputs:

        if program_input.cfd_software == "OpenFOAM":
            samplepts = read_openfoam_cfd_samplepts(cfd_input[3])
        elif program_input.cfd_software == "CFX":
            samplepts = read_openfoam_cfd_samplepts(cfd_input[3])
        else:
            raise ValueError(f"Unsupported CFD software: {program_input.cfd_software}")

        case = dat.CFDcase(
            V_free = cfd_input[0],
            Ma_free = cfd_input[1],
            rho_Free = cfd_input[2],
            samplepts = samplepts
        )

        cfd_cases.append(case)

    return cfd_cases