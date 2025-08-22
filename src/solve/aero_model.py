import numpy as np
from src.utils import dat
from src.solve import struct
from tqdm import tqdm



def local_piston_theory_disp(cquad4_panel, q_physical, grid_to_dof_mapping_mat, xi, eta):
    """
    Local piston theory (displacement form).
    Returns delta_p_unsteady at one Gauss point (xi, eta).
    """

    N = dat.shape_func(xi, eta)

    delta_P_panel = 0.0
    rho_a_pos = 0.0
    rho_a_neg = 0.0

    V_panel = np.zeros(3)
    u_ = np.zeros(3)

    for node_idx, nid in enumerate(cquad4_panel.nodes):
        node = cquad4_panel.nodes[nid]
        
        try:
            # look up node dofs x,y,z,Rx,Ry,Rz from q_physical with grid_to_dof_mapping_mat
            idx = np.where(grid_to_dof_mapping_mat[0, :] == nid)[0][0]
            dofs = q_physical[idx:idx+6]
            if len(dofs) < 6:
                raise ValueError("Incomplete DOFs")
        except (IndexError, ValueError):
            # if node dofs cant be found, they correspond to the constrained root nodes, still need to consider these but no displacment here
            dofs = np.zeros(6)

        r_i_ = dofs[:3]         # translational displacements
        theta_i_ = dofs[3:6]    # rotational displacements

        delta_P_panel += N[node_idx] * (node.p_y_pos - node.p_y_neg)

        rho_a_pos += N[node_idx] * (node.rho_y_pos * node.a_y_pos)
        rho_a_neg += N[node_idx] * (node.rho_y_neg * node.a_y_neg)

        # displacement vector at panel center


        #print("theta_i_.shape:", theta_i_.shape, node.r_.shape, "center-node shape:", (cquad4_panel.center - node.r_).shape)

        u_ += N[node_idx] * (r_i_ + np.cross(theta_i_, (cquad4_panel.center - node.r_)))
        V_panel += N[node_idx] * (node.v_y_pos_ - node.v_y_neg_)

    # normal displacement at this Gauss point
    delta_n_ = np.dot(u_, cquad4_panel.n_) * cquad4_panel.n_ #vector projection (denom is unit vec so magnitude 1 and div by 1)
    w_disp_ = np.dot(V_panel, delta_n_)

    # Return delta_p at this Gauss point (no integration here!)
    delta_p_unst_disp = delta_P_panel + (rho_a_pos + rho_a_neg) * w_disp_

    return delta_p_unst_disp



def local_piston_theory_velo(cquad4_panel, q_physical, grid_to_dof_mapping_mat, xi, eta):
    """
    Evaluate and return unsteady pressure at one Gauss point (xi, eta) on a CQUAD4 panel.
    """
    N = dat.shape_func(xi, eta)

    delta_P_gp = 0.0
    rho_a_pos = 0.0
    rho_a_neg = 0.0
    v_b_ = np.zeros(3)

    for node_idx, nid in enumerate(cquad4_panel.nodes):
        node = cquad4_panel.nodes[nid]

        try:
            # look up node dofs x,y,z,Rx,Ry,Rz from q_physical with grid_to_dof_mapping_mat
            idx = np.where(grid_to_dof_mapping_mat[0, :] == nid)[0][0]
            dofs = q_physical[idx:idx+6]
            if len(dofs) < 6:
                raise ValueError("Incomplete DOFs")
        except (IndexError, ValueError):
            # if node dofs cant be found, they correspond to the constrained root nodes, still need to consider these but no displacment here
            dofs = np.zeros(6)

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




def build_aero_matrix(cquad4_panels, phi, grid_to_dof_mapping_mat, LPT_func):

    n_dofs = phi.shape[0]
    n_modes = phi.shape[1]

    fin_struct = struct.iso_fin_structural_axis(cquad4_panels) #TODO: move to main

    aero_matrix = np.zeros((n_dofs, n_dofs))
    aero_col = dat.AeroMatColumn(grid_to_dof_mapping_mat)

    for j in tqdm(range(n_modes)):
        q_modal = np.zeros(n_modes)
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
                                    M_node_[0], 0.0, M_node_[2]]             
                        #NOTE: Drilling DOF is excluded (because of assumtions of NASTRAN CQUAD4 SHELL ELEMENTS)
                        

                    aero_col.add_dof_loads(nid, dof_loads)

        aero_matrix[:, j] = aero_col.col
        aero_col.clear()

    modal_aero_matrix = phi.T @ aero_matrix @ phi
    return modal_aero_matrix
    """NOTE: "FORCE" AND "UNSTEADY PRESSURE" SHOULD BE USED LOOSELY HERE BECAUSE THEY ARE DIMENSIONALIZED DIFFERENTLY"""
