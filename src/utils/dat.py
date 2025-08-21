import numpy as np
import pandas as pd
from src.utils import dat
from dataclasses import dataclass, field
from scipy.sparse import csr_matrix
from pyNastran.bdf.bdf import BDF
from pyNastran.op2.op2 import OP2

"""OpenFOAM sims assuming ideal gas:"""
GAMMA = 1.4
R_SPEC_AIR = 287.0024853 #J/kg

"""CFDresult abstraction"""

@dataclass
class CFDsamplepts:             # sampled CFD flow field on fin OML
    pressures: np.ndarray           # Static Pressures (Pa)
    densities: np.ndarray           # Density (kg/m^3)
    speed_of_sounds: np.ndarray     # (m/s)
    velocities: list[np.ndarray]    # (m/s)


@dataclass
class CFDcase:                  # a single result. Code setup for multiple cases for different flight conditions or linear flight reigimes
    V_free: float                   # Freestream speed (m/s)
    Mach_free: float                # Freestream Mach number
    rho_free: float                 # Freestream density (kg/m^3)
    samplepts: CFDsamplepts


@dataclass
class NASTRANsol103:
    model: BDF
    results: OP2
    phi: csr_matrix
    KGG: csr_matrix
    MGG: csr_matrix
    DOF: dict[int, int]
    n_dofs: int

### Gauss Coordinates ordered by node_idx

gauss_coords_xi_eta = [    
    [ -1/np.sqrt(3), -1/np.sqrt(3) ], 
    [ 1/np.sqrt(3), -1/np.sqrt(3) ],
    [ 1/np.sqrt(3), 1/np.sqrt(3) ],
    [ -1/np.sqrt(3), 1/np.sqrt(3) ]
]


def shape_func(xi, eta):
    N = [
        0.25 * (1 - xi) * (1 - eta),
        0.25 * (1 + xi) * (1 - eta),
        0.25 * (1 + xi) * (1 + eta),
        0.25 * (1 - xi) * (1 + eta),
    ]
    return N


"""
NODE (plus) abstraction 

y pos and y neg refer to the sides of the fin the flowfield is sampled at
"""
class node_plus:
    def __init__(self, r_=np.ndarray, p_y_pos=float, rho_y_pos=float, a_y_pos=float, v_y_pos_=float, p_y_neg=float, rho_y_neg=float, a_y_neg=float, v_y_neg_=float):

        self.r_ = r_

        self.p_y_pos = p_y_pos
        self.rho_y_pos = rho_y_pos
        self.a_y_pos = a_y_pos
        self.v_y_pos_ = v_y_pos_

        self.p_y_neg = p_y_neg
        self.rho_y_neg = rho_y_neg
        self.a_y_neg = a_y_neg
        self.v_y_neg_ = v_y_neg_




"""CQUAD4 element / Panel abstraction"""
"attr"
# list of node plus! 
# element normal vector

"methods"
# compute normal vector --> can do this on startup
# compute jacobian? --> can do this on startup?
# Local Piston Theory (1st order assuming harmonic motion)  --> element normal vector in this scope? or can we pass it in and call per node of element?

class cquad4_panel:
    def solve_center(self):
        coords = np.array([self.nodes[nid].r_ for nid in self.nodes])
        return coords.mean(axis=0)

    def solve_unit_normal_vec(self):
        coords = [node.r_ for _, node in self.nodes.items()]
        v1 = coords[1] - coords[0]  # G2 - G1
        v2 = coords[2] - coords[0]  # G3 - G1

        cross = np.cross(v1,v2)
        return cross / np.linalg.norm(cross)
    
    def compute_jacobian(self, xi, eta):
        pts = [node.r_ for _, node in self.nodes.items()]

        # shape function derivatives at (xi, eta)
        dN_dxi = np.array([
            -0.25 * (1 - eta),   # dN1/dxi
            0.25 * (1 - eta),   # dN2/dxi
            0.25 * (1 + eta),   # dN3/dxi
            -0.25 * (1 + eta)    # dN4/dxi
        ])

        dN_deta = np.array([
            -0.25 * (1 - xi),    # dN1/deta
            -0.25 * (1 + xi),    # dN2/deta
            0.25 * (1 + xi),    # dN3/deta
            0.25 * (1 - xi)     # dN4/deta
        ])

        dr_dxi = np.tensordot(dN_dxi, pts, axes=(0,0) )
        dr_deta = np.tensordot(dN_deta, pts, axes=(0,0) )

        #jacobian determinate is the mag of cross product
        normal = np.cross(dr_dxi, dr_deta)
        return np.linalg.norm(normal)
    

    def __init__(self, elem, node_lookup: dict[int, node_plus], fin_const_thickness):
        # Extract node IDs in Nastran's sequential order
        nid1, nid2, nid3, nid4 = elem.node_ids

        # Use node_lookup to fetch node_plus instances
        self.nodes = {
            nid1: node_lookup[nid1],
            nid2: node_lookup[nid2],
            nid3: node_lookup[nid3],
            nid4: node_lookup[nid4]
        }

        self.center = self.solve_center()
        self.n_ = self.solve_unit_normal_vec()
        self.t = fin_const_thickness


class AeroMatColumn:
    def __init__(self, grid_to_dof_mapping_mat):
        self.grid_to_dof_mapping_mat =grid_to_dof_mapping_mat
        self.col = np.zeros( len(self.grid_to_dof_mapping_mat[0]) )

    def clear(self):
        self.col.fill(0)

    def add_dof_loads(self, grid_id, dof_loads):
        # Find indices where grid_id matches the node ID row
        indices = np.where(self.grid_to_dof_mapping_mat[0] == grid_id)[0]

        # Add loads to corresponding DOF locations in self.col
        for i, idx in enumerate(indices):
            self.col[idx] += dof_loads[i]
    


class FlutterResultsCollector:
    def __init__(self):
        self.results = []

    def add_case(self, case: CFDcase, eigvals: np.ndarray):
        for mode_number, lam in enumerate(eigvals, start=1):
            sigma = lam.real
            omega = lam.imag
            freq = abs(omega) / (2 * np.pi)
            damping = -sigma / np.sqrt(sigma**2 + omega**2) if omega != 0 else np.nan

            self.results.append({
                "speed": case.V_free,
                "Mach": case.Mach_free,
                "rho": case.rho_free,
                "mode": mode_number,
                "real": sigma,
                "imag": omega,
                "freq": freq,
                "damping": damping
            })


    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.results)

    def save_csv(self, filename: str):
        df = self.to_dataframe()
        df.to_csv(filename, index=False)
