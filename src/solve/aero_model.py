import numpy as np
from numpy.linalg import eig
from src.utils import utils, dat
from collections import defaultdict
from solve import struct

"""
Parse the openfoam data and build all the node+ objects
"""
def build_node_plus_dict(model, openfoam_case):

    node_ids = sorted(model.nodes.keys()) #node_ids arranged in chronological order because openfoam dict in this order
    coords = np.array([model.nodes[nid].xyz for nid in node_ids])

    nodes = {}
    # Build dict of node_plus instances
    j=0 #j is the index of the openfoam sample points. Order of data is that ith nastran node corresponds to the jth and j+1th openfoam sample points
    for i, nid in enumerate(node_ids):

        nodes[nid] = dat.node_plus(
            r_=coords[nid],

            p_y_plus=(openfoam_case.samplepts.pressures[j]),
            rho_y_plus=(openfoam_case.samplepts.densities[j]),
            a_y_plus=np.sqrt(dat.GAMMA*openfoam_case.samplepts.temperatures[j]*dat.R_SPEC_AIR),
            u_y_plus_= openfoam_case.samplepts.velocities[j],

            #the sample point directly below is at the index (opposite side) + 1
            p_y_neg=(openfoam_case.samplepts.pressures[j+1]),
            rho_y_neg=(openfoam_case.samplepts.densities[j+1]),
            a_y_neg=np.sqrt(dat.GAMMA*openfoam_case.samplepts.temperatures[j+1]*dat.R_SPEC_AIR),
            u_y_neg_= openfoam_case.samplepts.velocities[j+1],
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
def local_piston_theory_disp(p, rho, a, u, cquad4_panel, q):

    ### only one dof will be excited

    #TODO: RESOLVE delta_n_ from displaced position


    w_disp_ = u_*delta_n_ # type: ignore
    return p + rho*a*w_disp_# type: ignore



def local_piston_theory_velo(p, rho, a, u, cquad4_panel, q_i, Phi, xi, eta):

    vel_dof_field = Phi @ q_i
    u_gauss_velo = np.zeros(3)
    r_gauss = interpolated_position(xi, eta)

    for node_idx, nid in enumerate(cquad4_panel.nodes):
        node = cquad4_panel.nodes[nid]

        dof_offset = 6 * nid
        v_trans = vel_dof_field[dof_offset + 0 : dof_offset + 3]
        omega = vel_dof_field[dof_offset + 3 : dof_offset + 6]
        r_node = node.r_
        r_rel = r_gauss - r_node

        shape_val = dat.shape_func(node_idx, xi, eta)
        u_node_velo = shape_val * (v_trans + np.cross(omega, r_rel))
        u_gauss_velo += u_node_velo

    n_vec = cquad4_panel.normal_at(xi, eta) #why????
    w_velo_ = np.dot(u_gauss_velo, n_vec)
    return p + rho * a * w_velo_








"""
Build A or B time domain modal aero matrix depending on the local piston theory passed in (displacement or velocity based).
"""
def build_aero_matrix(n_dofs, nodes, cquad4_panels, phi, grid_to_dof_mapping_mat, LPT_func):

    aero_matrix = np.zeros((n_dofs, n_dofs))
    aero_col = dat.AeroMatColumn(grid_to_dof_mapping_mat)

    for j in range(n_dofs):
        q_modal = np.zeros(n_dofs)
        q_modal[j] = 1.0
        q_physical = phi @ q_modal


        #entering this loop, how do we know which dof is excited?
        for cquad4_panel in cquad4_panels:

            for node_idx, nid in enumerate(cquad4_panel.nodes):
                node = cquad4_panel.nodes[nid]

                p_unst_pos_y = LPT_func(node.p_y_plus, node.rho_y_plus, node.a_y_plus, node.u_y_plus_, cquad4_panel, q_physical)
                p_unst_neg_y = LPT_func(node.p_y_neg, node.rho_y_neg, node.a_y_neg, node.u_y_neg_, cquad4_panel, q_physical)

                delta_p_unst = p_unst_pos_y - p_unst_neg_y

#NOTE: I THINK THIS IS WRONG IT SHOULD BE A SUM RIGHT?
                dF_panel_ = -delta_p_unst*cquad4_panel.n_*cquad4_panel.jacobian

                xi, eta = dat.gauss_coords(node_idx)
                F_node_ = dat.shape_func(node_idx, xi, eta) * dF_panel_


                #now sol the moments and assemble the vector
                elastic_axis_arm_1_ = struct.iso_fin_elastic_axis.interpolate_axis(node.r_[1], node.r_[2]) #MAKE THIS A CLASS NOT A FUNCTION
                moment_arm_ = node.r_ - elastic_axis_arm_1_

                M_node_ = np.cross(moment_arm_, F_node_)

                # M_y = 0 because no drilling dof!
                dof_loads = [ F_node_[0], F_node_[1], F_node_[2], M_node_[0], 0, M_node_[2] ]

                aero_col.add_dof_loads(nid, dof_loads)

        #append aero col to aero matrix

        aero_matrix[:, j] = aero_col.col
        aero_col.clear()

    modal_aero_matrix = phi.T @ aero_matrix @ phi
    return modal_aero_matrix

