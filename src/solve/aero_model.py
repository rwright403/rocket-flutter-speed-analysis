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




### local piston theory! - separate disp and velo terms for the different aero matrices A and B
"""
separate disp and velo terms
"""
def local_piston_theory_disp(cquad4_panel, q_physical, grid_to_dof_mapping_mat):

    delta_P_panel = 0.0

    rho_panel_pos = 0.0
    a_panel_pos = 0.0
    rho_panel_neg = 0.0
    a_panel_neg = 0.0

    V_panel = np.zeros(3)
    u_ = np.zeros(3)

    for node_idx, nid in enumerate(cquad4_panel.nodes):
        node = cquad4_panel.nodes[nid]

        #look up node dofs x,y,z,Rx,Ry,Rz from q_physical with grid_to_dof_mapping_mat
        idx = np.where(grid_to_dof_mapping_mat[0, :] == nid)[0][0]

        # Extract the 6 DOFs for this node as a NumPy array slice
        dofs = q_physical[idx : idx + 6]

        # First 3 are translational displacements
        r_i_ = dofs[:3]

        # Next 3 are rotational displacements
        theta_i_ = dofs[3:6]

        xi, eta = dat.gauss_coords(node_idx)


        delta_P_panel += dat.shape_func(node_idx, xi, eta) * (node.p_y_pos - node.p_y_neg)

        rho_panel_pos += dat.shape_func(node_idx, xi, eta) * node.rho_y_pos
        a_panel_pos += dat.shape_func(node_idx, xi, eta) * node.a_y_pos
        rho_panel_neg += dat.shape_func(node_idx, xi, eta) * node.rho_y_neg
        a_panel_neg += dat.shape_func(node_idx, xi, eta) * node.a_y_neg

        #u_ is the vector at the center of the element in the direction of displacement
        u_ += dat.shape_func(node_idx, xi, eta) * (r_i_ + theta_i_*(cquad4_panel.center - node.r_))
        V_panel += dat.shape_func(node_idx, xi, eta) * (node.u_y_pos - node.u_y_neg) #check this

    delta_n_ = np.dot(u_,cquad4_panel.n_)*cquad4_panel.n_
    w_disp_ = np.dot(V_panel, delta_n_)

    delta_p_unst_disp = delta_P_panel + (rho_panel_pos*a_panel_pos + rho_panel_neg*a_panel_neg)*w_disp_

    return delta_p_unst_disp




def local_piston_theory_velo(cquad4_panel, q_physical, grid_to_dof_mapping_mat):

    delta_P_panel = 0.0

    rho_panel_pos = 0.0
    a_panel_pos = 0.0
    rho_panel_neg = 0.0
    a_panel_neg = 0.0

    v_b_ = np.zeros(3)

    for node_idx, nid in enumerate(cquad4_panel.nodes):
        node = cquad4_panel.nodes[nid]

        #look up node dofs x,y,z,Rx,Ry,Rz from q_physical with grid_to_dof_mapping_mat
        idx = np.where(grid_to_dof_mapping_mat[0, :] == nid)[0][0]

        # Extract the 6 DOFs for this node as a NumPy array slice
        dofs = q_physical[idx : idx + 6]

        # First 3 are translational velocities
        v_i_ = dofs[:3]

        # Next 3 are rotational velocities
        omega_i_ = dofs[3:6]

        xi, eta = dat.gauss_coords(node_idx)


        delta_P_panel +=  dat.shape_func(node_idx, xi, eta) * (node.p_y_pos - node.p_y_neg)

        rho_panel_pos += dat.shape_func(node_idx, xi, eta) * node.rho_y_pos
        a_panel_pos += dat.shape_func(node_idx, xi, eta) * node.a_y_pos
        rho_panel_neg += dat.shape_func(node_idx, xi, eta) * node.rho_y_neg
        a_panel_neg += dat.shape_func(node_idx, xi, eta) * node.a_y_neg

        v_b_ += dat.shape_func(node_idx, xi, eta) * (v_i_ + omega_i_*(cquad4_panel.center - node.r_))
        
    w_velo_ = np.dot(v_b_, cquad4_panel.n_)

    delta_p_unst_velo = delta_P_panel + (rho_panel_pos*a_panel_pos + rho_panel_neg*a_panel_neg)*w_velo_

    return delta_p_unst_velo




"""
Build A or B time domain modal aero matrix depending on the local piston theory passed in (displacement or velocity based).
"""
def build_aero_matrix(n_dofs, nodes, cquad4_panels, phi, grid_to_dof_mapping_mat, LPT_func):

    fin_struct = struct.iso_fin_structural_axis(cquad4_panels)

    aero_matrix = np.zeros((n_dofs, n_dofs))
    aero_col = dat.AeroMatColumn(grid_to_dof_mapping_mat)

    for j in range(n_dofs):
        q_modal = np.zeros(n_dofs)
        q_modal[j] = 1.0
        q_physical = phi @ q_modal


        #entering this loop, how do we know which dof is excited?
        for cquad4_panel in cquad4_panels:

            #NO: I THINK THE LOCAL PISTON THEORY SHOULD BE OUTSIDE OF THE NODE_IDX LOOP ON THE PANEL LEVEL
            delta_p_unst = LPT_func(cquad4_panel, q_physical, grid_to_dof_mapping_mat)

            dF_panel_ = -delta_p_unst*cquad4_panel.n_*cquad4_panel.jacobian


            for node_idx, nid in enumerate(cquad4_panel.nodes):
                node = cquad4_panel.nodes[nid]

                xi, eta = dat.gauss_coords(node_idx)
                F_node_ = dat.shape_func(node_idx, xi, eta) * dF_panel_

                #now sol the moment arms with the fin struct class and solve the net moment:
                M_node_ = np.cross(fin_struct.bending_arm(node.r_), F_node_) + np.cross(fin_struct.torision_arm(node.r_), F_node_)

                                                                            # M_y = 0 because no drilling dof!
                dof_loads = [ F_node_[0], F_node_[1], F_node_[2], M_node_[0], 0, M_node_[2] ]

                aero_col.add_dof_loads(nid, dof_loads)

        aero_matrix[:, j] = aero_col.col
        aero_col.clear()

    modal_aero_matrix = phi.T @ aero_matrix @ phi
    return modal_aero_matrix