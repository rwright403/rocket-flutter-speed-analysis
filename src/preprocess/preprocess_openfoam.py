import pyvista as pv
import numpy as np
from pathlib import Path
from src.utils import utils, dat


class preprocess_openfoam():
    def __init__(self, program_input):
            
        ## I/O
        if not Path(program_input.openfoam_cfd_path).exists():
            raise FileNotFoundError(f"Input OpenFoam CFD file not found: {program_input.openfoam_cfd_path}")
        self.cfd_path = program_input.openfoam_cfd_path

        if not Path(program_input.openfoam_oml_path).exists():
            raise FileNotFoundError(f"Input OpenFoam oml file not found: {program_input.openfoam_oml_path}")
        self.oml_path = program_input.openfoam_oml_path




        self.freestream = dat.flowfield_point #outdated


        
        ## Interpolate

    def read_and_parse(self):
        raise NotImplementedError("TODO: Implement this method.")

        


"""  
def parse(cfd_mesh, oml_mesh):
    surface_flowfield_points = {}

    for point in oml_mesh.points:

        with runtime("one cell"):
            cell_index = cfd_mesh.find_containing_cell(point) #this is really slow
            elements = cfd_mesh.point_neighbors(cell_index)

            for idx in elements:
                cell = cfd_mesh.get_cell(idx)
                surface_flowfield_points[idx] = flowfield_point(cell.center,cfd_mesh.cell_data['p'],cfd_mesh.cell_data['rho'],cfd_mesh.cell_data['Ma'],cfd_mesh.cell_data['U'])

            break

    return surface_flowfield_points
"""