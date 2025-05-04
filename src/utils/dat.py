import numpy as np
from dataclasses import dataclass

"""
Flowfield point defined at the centroid of a NASTRAN CQUAD4 EID
"""
@dataclass
class flowfield_point:
    cquad4_eid : int #or just put in a dict?
    el_norm : np.ndarray
    centroid : np.ndarray

    p : float
    rho : float
    a : float #might need to use Ma
    u : np.ndarray

class flutter_node:
    nas_node_id : int #or just put in a dict?
