### Program Ctrl input:
"""
>f_max is the maximum frequency [rad/s] to define the range of modes analyzed for flutter from nastran
>f_min is the minimum frequency [rad/s] to define the range of modes analyzed for flutter from nastran
>f_pcnt_conv is the percentage difference between the guessed frequency and resolved frequency. Used to define "converged"
"""
f_max = 10000 # rad/s
f_min = 50 # rad/s

max_iter = 200
omega_pcnt_conv = 10 #%

output_filename = "out.csv"

### OpenFOAM input files for each relevant flow speed the user wants to analyze:
# Dictionary format: {freestream velocity speed (m/s) (float): vtk_path (str)}
openfoam_files = {
    343 : "~/OpenFOAM/rwright-11/run/Ma1.5_AoA0_R4_rhoPimpleFoam/VTK/Ma1.5_AoA0_R4_rhoPimpleFoam_896.vtk",
    # Add more entries like:
    # 686 : "~/OpenFOAM/.../Ma2.0_case.vtk",
    # 1029: "~/OpenFOAM/.../Ma3.0_case.vtk"
}

### Altair Hyperworks (NASTRAN) input files:
"""
> .bdf
> .op2
> .mat
"""

nastran_bdf_path = r"./_old/_old-1/model/test-case-3-learning/v3/tc3-v3-sol-103.bdf"
nastran_op2_path = r"./_old/_old-1/model/test-case-3-learning/v3/tc3-v3-sol-103.op2"
nastran_mat_path = r"./src/testing.full.mat"
