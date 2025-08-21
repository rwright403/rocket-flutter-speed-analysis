### Program Ctrl input:

output_filename = "out.csv"

### Select the cfd software used to generate sample point output:
# "OpenFOAM"
# "CFX"

cfd_software = "CFX"

### input files for each relevant flow speed the user wants to analyze:
# Dictionary format: {freestream velocity speed (m/s) (float): vtk_path (str)}
cfd_inputs = [
    [548.8, 1.6, 1.225, "~/rocket-flutter-speed-analysis/openfoam_cases/[3]-80-pcnt-test-fin/postProcessing/sample/0/"],
    # Add more entries like:
    # [V_free, Ma_free, rho_free, "~/rocket-flutter-speed-analysis/openfoam_cases/[3]-80-pcnt-test-fin/.../0/"],
]

### Altair Hyperworks (NASTRAN) input files:
"""
> .bdf
> .op2
> .mat
"""

nastran_bdf_path = r"./_old/_old-1/model/test-case-3-learning/v3/tc3-v3-sol-103.bdf"
nastran_op2_path = r"./_old/_old-1/model/test-case-3-learning/v3/tc3-v3-sol-103.op2"
nastran_mat_path = r"./src/testing.full.mat"