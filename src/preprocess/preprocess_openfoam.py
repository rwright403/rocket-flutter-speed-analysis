import pyvista as pv
import numpy as np
from dataclasses import dataclass

from src.utils.time_feat_g_eazy_and_olivver_the_kid import runtime

from concurrent.futures import ThreadPoolExecutor

@dataclass
class flowfield_point:
    pos : np.ndarray
    p : float
    rho : float
    Ma : float
    u : np.ndarray

    

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
preprocess results from openfoam to create a surface flow field #TODO: add interpolation here?
"""
class preprocess_openfoam():
    def __init__(self, program_input):
    
        with runtime("read openfoam"):
            self.cfd_path = program_input.openfoam_cfd_path
            self.oml_path = program_input.openfoam_oml_path

            cfd_mesh = pv.read(self.cfd_path)
            oml_mesh = pv.read(self.oml_path)
        print(f"     (for reference) read {oml_mesh.n_points} points from rocket oml")


        with runtime("parse"):
            surface_flowfield_points = parse(cfd_mesh, oml_mesh)
            

        #interpolate()






