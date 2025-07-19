import numpy as np
from numpy.linalg import eig
from src.utils import utils, dat
from collections import defaultdict
from solve import struct

"""
Parse the openfoam data and build all the node+ objects
"""
def build_node_plus_dict(model, openfoam_data):

    node_ids = sorted(model.nodes.keys()) #node_ids arranged in chronological order because openfoam dict in this order
    coords = np.array([model.nodes[nid].xyz for nid in node_ids])

    nodes = {}
    # Build dict of node_plus instances
    j=0 #j is the index of the openfoam sample points. Order of data is that ith nastran node corresponds to the jth and j+1th openfoam sample points
    for i, nid in enumerate(node_ids):

        nodes[nid] = dat.node_plus(
            r_=coords[nid],

            p_y_plus=(openfoam_data.pressures[j]),
            rho_y_plus=(openfoam_data.densities[j]),
            a_y_plus=np.sqrt(dat.GAMMA*openfoam_data.temperatures[j]*dat.R_SPEC_AIR),
            u_y_plus_= openfoam_data.velocities[j],

            #the sample point directly below is at the index (opposite side) + 1
            p_y_neg=(openfoam_data.pressures[j+1]),
            rho_y_neg=(openfoam_data.densities[j+1]),
            a_y_neg=np.sqrt(dat.GAMMA*openfoam_data.temperatures[j+1]*dat.R_SPEC_AIR),
            u_y_neg_= openfoam_data.velocities[j+1],
        )
        j +=2

    return nodes


def build_cquad4_panel_array(nas_elements, nodes):
    cquad4_panels = []

    for _, elem in nas_elements.items(): #NOTE: I BELIEVE THIS IS CORRECT BUT MIGHT NEED TO DOUBLE CHECK
        if elem.type == 'CQUAD4':
            cquad4_panel = dat.cquad4_panel(elem, nodes)
            cquad4_panels.append(cquad4_panel)
        else:
            raise NotImplementedError("Nastran FEM contains elements that are not CQUAD4. This program only supports CQUAD4 elements.")

    return cquad4_panels




### local piston theory! - separate disp and velo terms for the different aero matrices A and B
"""
separate disp and velo terms
"""
def local_piston_theory_disp(p, rho, a, u, cquad4_panel, q_i):

    ### only one general coord will be excited,



    w_disp_ = u_*delta_n_ # type: ignore
    return p + rho*a*w_disp_# type: ignore



def local_piston_theory_velo(p, rho, a, u, cquad4_panel, q_i):

    u_b_ = #TODO

    w_velo_ = u_b_*n_ # type: ignore
    return p + rho*a*w_velo_# type: ignore



"""
solve the force of lift contribution from panel on a node
return aero force (vector)
"""
def solve_aero_force_on_node(node, xi, eta, cquad4_panel, local_piston_theory_func, q_i):


    p_unst_pos_y = local_piston_theory_func(node.p_y_plus, node.rho_y_plus, node.a_y_plus, node.u_y_plus_, cquad4_panel, q_i)
    p_unst_neg_y = local_piston_theory_func(node.p_y_plus, node.rho_y_plus, node.a_y_plus, node.u_y_plus_, cquad4_panel, q_i)

    delta_p_unst = p_unst_pos_y - p_unst_neg_y #MIGHT NEED TO CHECK SIGNS

    dF_panel = -delta_p_unst*cquad4_panel.n_*cquad4_panel.jacobian
    
    ### put node shape function in node+ ?
    # F on node += node.shape_func * dF_panel

    F = shape_func(xi, eta) * dF_panel #TODO: IMPLEMENT SHAPE FUNCTION 

        
    return F











"""
Build A or B time domain modal aero matrix depending on the local piston theory passed in (displacement or velocity based).
"""
def build_aero_matrix(n_modes, nodes, cquad4_panels, Phi, LPT_func):

    aero_matrix = np.zeros((n_modes, n_modes))

    for j in range(n_modes):
        q = np.zeros(n_modes)
        q[j] = 1.0
        mode_dof_field = Phi @ q  # convert generalized coords unit displacement or unit velocity to physical space

        force_dof_map = defaultdict(lambda: np.zeros(6)) #KEY - node id, #VALUE - array 6 items each corresponding to a dof

        #entering this loop, how do we know which node is excited?
        for cquad4_panel in cquad4_panels:
            for (node, xi, eta) in [
                (cquad4_panel.nodes[0].values(), -1/np.sqrt(3), -1/np.sqrt(3)),
                (cquad4_panel.nodes[1].values(),  1/np.sqrt(3), -1/np.sqrt(3)),
                (cquad4_panel.nodes[2].values(),  1/np.sqrt(3),  1/np.sqrt(3)),
                (cquad4_panel.nodes[3].values(), -1/np.sqrt(3),  1/np.sqrt(3)),
            ]:
    
                #how to know if the node is the one that is excited? - can get the node id from keys?

                if node.

                F_node = solve_aero_force_on_node(
                    node, xi, eta,
                    cquad4_panel, LPT_func, q_i
                )

        ### put this inside F_node? i feel like nodal force doesn't make sense its applied to each dof?
                elastic_axis_arm_1 = struct.solve_elastic_axis_isotropic_fin()
                #add panel contribution to the total force on the node:
                #                                         X,         Y,         Z,                    Mx,             My,             Mz
                #THIS IS WRONG REPLACE W CROSS PRODUCT force_dof_map{cquad4_panel.nid1} += [ F_node[0], F_node[1], F_node[2], (0.5*cquad4_panel.t*F_node[0]), 0, (elastic_axis_arm_1*F_node[2]) ]


        f_aero_dofs = utils.translate_node_force_dict_to_dof_col_vector(force_dof_map)
        aero_matrix[:, j] = Phi.T @ f_aero_dofs 

    return aero_matrix



"""
    force_dof_map = defaultdict(lambda: np.zeros(6)) #KEY - node id, #VALUE - array 6 items each corresponding to a dof
        
    for cquad4_panel in cquad4_panels:

        cquad4_panel.n_

        cmplx_amp_n1 = 1 #TODO: EXTRACT COMPLEX AMPLITUDE FROM MODE SHAPE
        F_1 = solve_aero_force_on_node(omega_guess, (-1/np.sqrt(3)), (-1/np.sqrt(3)), cquad4_panel.n1, cquad4_panel, cmplx_amp_n1)
        elastic_axis_arm_1 = struct.solve_elastic_axis_isotropic_fin
        #add panel contribution to the total force on the node:
        #                       X,      Y, Z,                    Mx, My,                      Mz
#TODO: FIX!        force_dof_map{cquad4_panel.nid1} += [ 0, F_1, 0, (0.5*cquad4_panel.t*F_1), 0, (elastic_axis_arm_1*F_1) ]


        cmplx_amp_n2 = 1 #TODO: EXTRACT COMPLEX AMPLITUDE FROM MODE SHAPE
        F_2 =solve_aero_force_on_node(omega_guess, (1/np.sqrt(3)), (-1/np.sqrt(3)), cquad4_panel.n2, cquad4_panel, cmplx_amp_n2)
        elastic_axis_arm_2 = struct.solve_elastic_axis_isotropic_fin
#TODO: FIX!        force_dof_map{cquad4_panel.nid2} += [ 0, F_2, 0, (0.5*cquad4_panel.t*F_2), 0, (elastic_axis_arm_2*F_2) ] 


        cmplx_amp_n3 = 1 #TODO: EXTRACT COMPLEX AMPLITUDE FROM MODE SHAPE
        F_3 =solve_aero_force_on_node(omega_guess, (1/np.sqrt(3)), (1/np.sqrt(3)), cquad4_panel.n3, cquad4_panel, cmplx_amp_n3)
        elastic_axis_arm_3= struct.solve_elastic_axis_isotropic_fin
#TODO: FIX!        force_dof_map{cquad4_panel.nid3} += [ 0, F_3, 0, (0.5*cquad4_panel.t*F_3), 0, (elastic_axis_arm_3*F_3) ] 


        cmplx_amp_n4 = 1 #TODO: EXTRACT COMPLEX AMPLITUDE FROM MODE SHAPE
        F_4 =solve_aero_force_on_node(omega_guess, (-1/np.sqrt(3)), (1/np.sqrt(3)), cquad4_panel.n4, cquad4_panel, cmplx_amp_n4)
        elastic_axis_arm_4 = struct.solve_elastic_axis_isotropic_fin
#TODO: FIX!        force_dof_map{cquad4_panel.nid4} += [ 0, F_4, 0, (0.5*cquad4_panel.t*F_4), 0, (elastic_axis_arm_4*F_4) ] 

    matrix = format_unsteady_aero_matrix(force_dof_map, nodes)
    return matrix
"""
