def local_piston_theory_velo(p, rho, a, u_inf, cquad4_panel, q_i, Phi, xi, eta):
    vel_dof_field = Phi @ q_i
    u_gauss_velo = np.zeros(3)
    r_gauss = cquad4_panel.interpolated_position(xi, eta)

    for node_idx, node in enumerate(cquad4_panel.nodes):
        dof_offset = 6 * node.index
        v_trans = vel_dof_field[dof_offset + 0 : dof_offset + 3]
        omega = vel_dof_field[dof_offset + 3 : dof_offset + 6]
        r_node = node.r_
        r_rel = r_gauss - r_node

        shape_val = shape_func(node_idx, xi, eta)
        u_node_velo = shape_val * (v_trans + np.cross(omega, r_rel))
        u_gauss_velo += u_node_velo

    n_vec = cquad4_panel.normal_at(xi, eta)
    w_velo_ = np.dot(u_gauss_velo, n_vec)
    return p + rho * a * w_velo_


