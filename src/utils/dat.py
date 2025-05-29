import numpy as np
from dataclasses import dataclass

"""
Flowfield point defined at the centroid of a NASTRAN CQUAD4 EID
"""
@dataclass
class flowfield_point:
    p : float
    rho : float
    a : float #might need to use Ma
    u : np.ndarray



@dataclass
class cquad4_aero_panel:
    # record corresponding cquad4_eid as a key of a dict
    el_norm : np.ndarray
    centroid : np.ndarray
    flow_pt : flowfield_point



@dataclass
class aero_node:
    # record corresponding nas_node_id as a key of a dict
    f_real : np.ndarray
    f_img : np.ndarray