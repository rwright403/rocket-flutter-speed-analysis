import numpy as np
### Program Ctrl input:

sweep_velocities = np.linspace(300, 1200, 18)

output_filename = "out.csv"

### Select the cfd software used to generate sample point output:
# "OpenFOAM"
# "CFX"

cfd_software = "CFX"

### input files for each relevant flow speed the user wants to analyze:
# Dictionary format: {freestream velocity speed (m/s) (float): vtk_path (str)}
cfd_inputs = [
    [548.8, 1.6, 1.225, "./src/inputs/AOA0_vector.csv"],
    # Add more entries like:
    # [V_free, Ma_free, rho_free, "./[3]-80-pcnt-test-fin/.../0/"],
]

### Altair Hyperworks (NASTRAN) input files:
"""
> .bdf
> .op2
> .mat
"""

nastran_bdf_path = r"./src/inputs/A2_fin.pch"
nastran_op2_path = r"./src/inputs/A2_fin.op2"
nastran_mat_path = r"./src/inputs/A2_fin.full.mat"