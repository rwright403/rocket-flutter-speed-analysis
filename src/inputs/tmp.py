
### OpenFOAM input files:
"""
>
>
"""
#convert openfoam results and rocket boundary surface to .vtk format and enter paths
openfoam_cfd_path = r"~/OpenFOAM/rwright-11/run/Ma1.5_AoA0_R4_rhoPimpleFoam/VTK/Ma1.5_AoA0_R4_rhoPimpleFoam_896.vtk" # ~ means rel to home btw
openfoam_oml_path = r"~/OpenFOAM/rwright-11/run/Ma1.5_AoA0_R4_rhoPimpleFoam/VTK/wallPatch/wallPatch_896.vtk"


### NASTRAN input files:
"""
> .bdf
> .op2
> .op4
"""

nastran_bdf_path = r"./_old/_old-1/model/test-case-3-learning/v3/tc3-v3-sol-103.bdf"
nastran_op2_path = r"./_old/_old-1/model/test-case-3-learning/v3/tc3-v3-sol-103.op2"
#nastran_op4_path = r"./_old/_old-1/model/test-case-3-learning/v3/tc3-v3-sol-103.op4"