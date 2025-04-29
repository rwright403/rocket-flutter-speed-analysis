import numpy as np
from dataclasses import dataclass


@dataclass
class flowfield_point:
    pos : np.ndarray
    p : float
    rho : float
    a : float #might need to use Ma
    u : np.ndarray




@dataclass
class node:
    flow : flowfield_point
    norm : np.array
