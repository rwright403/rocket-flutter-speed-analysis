import numpy as np
from src.utils import dat
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
            raise NotImplementedError("Input Nastran FEM contains elements that are not CQUAD4. This program only supports CQUAD4 elements.")

    return cquad4_panels



def local_piston_theory_disp(cquad4_panel, q_physical, grid_to_dof_mapping_mat, xi, eta):
    """
    Local piston theory (displacement form).
    Returns Δp_unsteady at one Gauss point (xi, eta).
    """

    N = dat.shape_func(xi, eta)

    delta_P_panel = 0.0
    rho_a_pos = 0.0
    rho_a_neg = 0.0

    V_panel = np.zeros(3)
    u_ = np.zeros(3)

    for node_idx, nid in enumerate(cquad4_panel.nodes):
        node = cquad4_panel.nodes[nid]

        # look up node dofs x,y,z,Rx,Ry,Rz from q_physical with grid_to_dof_mapping_mat
        idx = np.where(grid_to_dof_mapping_mat[0, :] == nid)[0][0]
        dofs = q_physical[idx : idx + 6]

        r_i_ = dofs[:3]         # translational displacements
        theta_i_ = dofs[3:6]    # rotational displacements

        delta_P_panel += N[node_idx] * (node.p_y_pos - node.p_y_neg)

        rho_a_pos += N[node_idx] * (node.rho_y_pos * node.a_y_pos)
        rho_a_neg += N[node_idx] * (node.rho_y_neg * node.a_y_neg)

        # displacement vector at panel center
        u_ += N[node_idx] * (r_i_ + np.cross(theta_i_, (cquad4_panel.center - node.r_)))
        V_panel += N[node_idx] * (node.v_y_pos - node.v_y_neg)

    # normal displacement at this Gauss point
    delta_n_ = np.dot(u_, cquad4_panel.n_) * cquad4_panel.n_ #vector projection (denom is unit vec so magnitude 1 and div by 1)
    w_disp_ = np.dot(V_panel, delta_n_)

    # Return delta_p at this Gauss point (no integration here!)
    delta_p_unst_disp = delta_P_panel + (rho_a_pos + rho_a_neg) * w_disp_

    return delta_p_unst_disp






def local_piston_theory_velo(cquad4_panel, q_physical, grid_to_dof_mapping_mat, xi, eta):
    """
    Evaluate unsteady pressure at one Gauss point (xi, eta) on a CQUAD4 panel.
    """
    N = dat.shape_func(xi, eta)

    delta_P_gp = 0.0
    rho_a_pos = 0.0
    rho_a_neg = 0.0
    v_b_ = np.zeros(3)

    for node_idx, nid in enumerate(cquad4_panel.nodes):
        node = cquad4_panel.nodes[nid]

        # look up node DOFs in physical space
        idx = np.where(grid_to_dof_mapping_mat[0, :] == nid)[0][0]
        dofs = q_physical[idx: idx + 6]

        v_i_ = dofs[:3]      # translational velocities
        omega_i_ = dofs[3:6] # rotational velocities

        # interpolate panel state
        delta_P_gp += N[node_idx] * (node.p_y_pos - node.p_y_neg)
        rho_a_pos  += N[node_idx] * (node.rho_y_pos * node.a_y_pos)
        rho_a_neg  += N[node_idx] * (node.rho_y_neg * node.a_y_neg)
        v_b_       += N[node_idx] * (v_i_ + np.cross(omega_i_, (cquad4_panel.center - node.r_)))

    # normal velocity at Gauss point
    w_velo_ = np.dot(v_b_, cquad4_panel.n_)

    # unsteady pressure at this Gauss point
    delta_p_gp = delta_P_gp + (rho_a_pos + rho_a_neg) * w_velo_

    return delta_p_gp




def build_aero_matrix(n_dofs, cquad4_panels, phi, grid_to_dof_mapping_mat, LPT_func):

    fin_struct = struct.iso_fin_structural_axis(cquad4_panels)

    aero_matrix = np.zeros((n_dofs, n_dofs))
    aero_col = dat.AeroMatColumn(grid_to_dof_mapping_mat)

    for j in range(n_dofs):
        q_modal = np.zeros(n_dofs)
        q_modal[j] = 1.0
        q_physical = phi @ q_modal

        for cquad4_panel in cquad4_panels:

            for xi, eta in dat.gauss_coords_xi_eta:  # loop Gauss points

                delta_p_gp = LPT_func(cquad4_panel, q_physical, grid_to_dof_mapping_mat, xi, eta)

                dF_gp = -delta_p_gp * cquad4_panel.n_ * cquad4_panel.compute_jacobian(xi, eta) # * gauss weight, which = 1 for our case

                # distribute Gauss point contribution to nodes
                N = dat.shape_func(xi, eta)

                for node_idx, nid in enumerate(cquad4_panel.nodes):
                    node = cquad4_panel.nodes[nid]
                    F_node_ = N[node_idx] * dF_gp

                    # nodal moment arms
                    M_node_ = (np.cross(fin_struct.bending_arm(node.r_), F_node_) +
                               np.cross(fin_struct.torision_arm(node.r_), F_node_))

                    dof_loads = [F_node_[0], F_node_[1], F_node_[2],
                                 M_node_[0], 0.0, M_node_[2]]             #NOTE: Drilling DOF is excluded (because of assumtions of NASTRAN CQUAD4 SHELL ELEMENTS)

                    aero_col.add_dof_loads(nid, dof_loads)

        aero_matrix[:, j] = aero_col.col
        aero_col.clear()

    modal_aero_matrix = phi.T @ aero_matrix @ phi
    return modal_aero_matrix

