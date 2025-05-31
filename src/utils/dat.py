import numpy as np
from dataclasses import dataclass


"""NODE (plus) abstraction """
"attr"
# P, rho, a,
#F_aero_

"methods" # - none? dataclass?

@dataclass
class node_plus:
    r_ : np.ndarray

    p : float
    rho : float
    a : float #might need to use Ma
    u_ : np.ndarray

    F_aero_ : np.ndarray = np.array([0,0,0])





"""CQUAD4 element / Panel abstraction"""
"attr"
# list of node plus! 
# element normal vector

"methods"
# compute normal vector --> can do this on startup
# compute jacobian? --> can do this on startup?
# Local Piston Theory (1st order assuming harmonic motion)  --> element normal vector in this scope? or can we pass it in and call per node of element?

class cquad4_panel:
    def solve_unit_normal_vec(self):
        v1 = self.n2.r_ - self.n1.r_
        v2 = self.n3.r_ - self.n1.r_

        cross = np.cross(v1,v2)
        return cross / np.linalg.norm(cross)
    
    def compute_jacobian(self):

        pts = np.array([ self.n1.r_, self.n2.r_, self.n3.r_, self.n4.r_ ])

        dN_dxi = np.array([
            -(1-(-1/np.sqrt(3))),   # dN1/dxi at eta = -1/sqrt(3)
            (1-(-1/np.sqrt(3))),    # dN2/dxi at eta = -1/sqrt(3)
            (1+(1/np.sqrt(3))),     # dN3/dxi at eta = 1/sqrt(3)
            -(1+(1/np.sqrt(3)))     # dN4/dxi at eta = 1/sqrt(3)
        ]) * 0.25

        dN_deta = np.array([
            -(1-(-1/np.sqrt(3))),   # dN1/deta at xi = -1/sqrt(3)
            (1-(1/np.sqrt(3))),     # dN2/deta at xi = 1/sqrt(3)
            (1+(1/np.sqrt(3))),     # dN3/deta at xi = 1/sqrt(3)
            -(1+(-1/np.sqrt(3)))    # dN4/deta at xi = -1/sqrt(3)
        ]) * 0.25

        dr_dxi = np.tensordot(dN_dxi, pts, axes=(0,0) )
        dr_deta = np.tensordot(dN_deta, pts, axes=(0,0) )

        #jacobian determinate is the mag of cross product
        normal = np.cross( dr_dxi, dr_deta )
        return np.linalg.norm(normal)


    def __init__(self):
        ###logic here to take pynastran cquad4 type and extract essential info

        self.n1 : node_plus # need to define the node plus on init which is ok!
        self.n2 : node_plus
        self.n3 : node_plus
        self.n4 : node_plus

        self.u_norm = self.solve_unit_normal_vec()
        self.jacobian = self.compute_jacobian()

        
        


    

