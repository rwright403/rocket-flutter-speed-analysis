### Program Ctrl input:
"""
>f_max is the maximum frequency [rad/s] to define the range of modes analyzed for flutter from nastran
>f_min is the minimum frequency [rad/s] to define the range of modes analyzed for flutter from nastran
>f_pcnt_conv is the percentage difference between the guessed frequency and resolved frequency. Used to define "converged"
"""
f_max = # rad/s
f_min = # rad/s

max_iter = # unitless
omega_pcnt_conv = # %

output_filename = # "out_str.csv"

### OpenFOAM input files for each relevant flow speed the user wants to analyze:
# Dictionary format: {freestream velocity speed (m/s) (float): vtk_path (str)}
openfoam_files = {
    
    # Add more entries like:
    # 686 : "~/OpenFOAM/.../Ma2.0_case.vtk",
    # 1029: "~/OpenFOAM/.../Ma3.0_case.vtk",
}

### Altair Hyperworks (NASTRAN) input files:
"""
> .bdf
> .op2
> .mat
"""

nastran_bdf_path = #r" ./filepath here! "
nastran_op2_path = #r" ./filepath here! "
nastran_mat_path = #r" ./filepath here! "
