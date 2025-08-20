### Program Ctrl input:

output_filename = "out.csv"

### Select the cfd software used to generate sample point output:
# "OpenFOAM"
# "CFX"

cfd_software = "CFX"

### input files for each relevant flow speed the user wants to analyze:
# Dictionary format: {freestream velocity speed (m/s) (float): vtk_path (str)}
cfd_inputs = [
    [400, 2.0, 1.221, "~/rocket-flutter-speed-analysis/src/inputs/A2/AOA0_vector.csv"],
    # Add more entries like:
    # [V_free, Ma_free, rho_free, "~/rocket-flutter-speed-analysis/openfoam_cases/[3]-80-pcnt-test-fin/.../0/"],
]

### Altair Hyperworks (NASTRAN) input files:
"""
> .bdf
> .op2
> .mat
"""

nastran_bdf_path = r"~/rocket-flutter-speed-analysis/src/inputs/A2/A2_fin.fem"
nastran_op2_path = r"~/rocket-flutter-speed-analysis/src/inputs/A2/A2_fin.op2"
nastran_mat_path = r"~/rocket-flutter-speed-analysis/src/inputs/A2/A2_fin.full.mat"