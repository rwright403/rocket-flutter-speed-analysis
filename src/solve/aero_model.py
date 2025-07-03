import numpy as np
from numpy.linalg import eig
from src.utils import utils, dat
from collections import defaultdict
from solve import struct

"""
Parse the openfoam data and build all the node+ objects
"""
def build_node_plus_dict(model, openfoam_data):

    node_ids = sorted(model.nodes.keys()) #node_ids arranged in chronological order 
    coords = np.array([model.nodes[nid].xyz for nid in node_ids])

    nodes = {}
    # Build list of node_plus instances
    j=0
    for i, nid in enumerate(node_ids):

        nodes[nid] = dat.node_plus(
            r_=coords[nid],

            p_y_plus=(openfoam_data.pressures[j]),
            rho_y_plus=(openfoam_data.densities[j]),
            a_y_plus=np.sqrt(dat.GAMMA*openfoam_data.temperatures[j]*dat.R_SPEC_AIR),
            u_y_plus_= openfoam_data.velocites[j],

            p_y_neg=(openfoam_data.pressures[j+1]),
            rho_y_neg=(openfoam_data.densities[j+1]),
            a_y_neg=np.sqrt(dat.GAMMA*openfoam_data.temperatures[j+1]*dat.R_SPEC_AIR),
            u_y_neg_= openfoam_data.velocites[j+1],
        )
        j +=2

    return nodes


def build_cquad4_panel_array(struct_harmonics, nodes):
    cquad4_panels = []

    for eid, elem in struct_harmonics.model.elements.items(): #NOTE: I BELIEVE THIS IS CORRECT BUT MIGHT NEED TO DOUBLE CHECK
        if elem.type == 'CQUAD4':
            cquad4_panel = dat.cquad4_panel(elem, nodes)
            cquad4_panels.append(cquad4_panel)

    return cquad4_panels




### local piston theory!
    #def local_piston_theory(): #NOTE: or put this as a method in the aero panel class or in the node class?
    # how to deal with 2 sides? 
    # --> define a + unst. pressure and a - unst. pressure?

    ### does this work here???? normal vector is an element parameter?
    ### should we create a list of unsteady pressures in the same order as the nastran nodes?
def local_piston_theory(p, rho, a, u, n_, omega, cmplx_amp):

    delta_n_ = - TODO

    u_b_ = 1j * omega * cmplx_amp

    w_ = u_*delta_n_ + u_b_*n_ # type: ignore

    return p + rho*a *w_ # type: ignore


"""
solve the force of lift contribution from panel on a node
return aero force
"""
def solve_aero_force(omega, xi, eta, node, cquad4_panel, cmplx_amp):
        


        ### not sure if its cmplx_amp or if its mode shape, need to figure out LPT

        
    p_unst_pos_y = local_piston_theory(node.p_y_plus, node.rho_y_plus, node.a_y_plus, node.u_y_plus_, cquad4_panel.n_, omega, cmplx_amp)
    p_unst_neg_y = local_piston_theory(node.p_y_plus, node.rho_y_plus, node.a_y_plus, node.u_y_plus_, cquad4_panel.n_, omega, cmplx_amp)

    p_unst = p_unst_pos_y - p_unst_neg_y #MIGHT NEED TO CHECK SIGNS

    dF_panel = -p_unst*cquad4_panel.n_*cquad4_panel.jacobian
    
    ### put node shape function in node+ ?
    # F on node += node.shape_func + dF_panel

    F = 

        
    return F










### BAD!!!
def format_unsteady_aero_matrix(force_dof_map, nodes):

    ### REORDER DOFS TO MATCH NASTRAN DOF
    Q_modal = 1


    ### TRANSFORM AERO MATRIX TO MODAL SPACE
    #Q_modal = utils.trans_matrix_phys_to_modal(phi, Q_phys)
    return Q_modal




### BUILD AERO MATRIX IN FREQUENCY DOMAIN AND PHYSICAL SPACE
def build_unsteady_aero_matrix(omega_guess, mode_shape, nodes, cquad4_panels):

    force_dof_map = defaultdict(lambda: np.zeros(6)) #KEY - node id, #VALUE - array 6 items each corresponding to a dof
        
    for cquad4_panel in cquad4_panels:

        cquad4_panel.n_

        cmplx_amp_n1 = 1 #TODO: EXTRACT COMPLEX AMPLITUDE FROM MODE SHAPE
        F_1 = solve_aero_force(omega_guess, (-1/np.sqrt(3)), (-1/np.sqrt(3)), cquad4_panel.n1, cquad4_panel, cmplx_amp_n1)
        elastic_axis_arm_1 = struct.solve_elastic_axis_isotropic_fin
        #add panel contribution to the total force on the node:
        #                       X,      Y, Z,                    Mx, My,                      Mz
        force_dof_map{n1id} += [ 0, F_1, 0, (0.5*cquad4_panel.t*F_1), 0, (elastic_axis_arm_1*F_1) ]


        cmplx_amp_n2 = 1 #TODO: EXTRACT COMPLEX AMPLITUDE FROM MODE SHAPE
        F_2 =solve_aero_force(omega_guess, (1/np.sqrt(3)), (-1/np.sqrt(3)), cquad4_panel.n2, cquad4_panel, cmplx_amp_n2)
        elastic_axis_arm_2 = struct.solve_elastic_axis_isotropic_fin
        force_dof_map{n2id} += [ 0, F_2, 0, (0.5*cquad4_panel.t*F_2), 0, (elastic_axis_arm_2*F_2) ] 


        cmplx_amp_n3 = 1 #TODO: EXTRACT COMPLEX AMPLITUDE FROM MODE SHAPE
        F_3 =solve_aero_force(omega_guess, (1/np.sqrt(3)), (1/np.sqrt(3)), cquad4_panel.n3, cquad4_panel, cmplx_amp_n3)
        elastic_axis_arm_3= struct.solve_elastic_axis_isotropic_fin
        force_dof_map{n3id} += [ 0, F_3, 0, (0.5*cquad4_panel.t*F_3), 0, (elastic_axis_arm_3*F_3) ] 


        cmplx_amp_n4 = 1 #TODO: EXTRACT COMPLEX AMPLITUDE FROM MODE SHAPE
        F_4 =solve_aero_force(omega_guess, (-1/np.sqrt(3)), (1/np.sqrt(3)), cquad4_panel.n4, cquad4_panel, cmplx_amp_n4)
        elastic_axis_arm_4 = struct.solve_elastic_axis_isotropic_fin
        force_dof_map{n4id} += [ 0, F_4, 0, (0.5*cquad4_panel.t*F_4), 0, (elastic_axis_arm_4*F_4) ] 

    Q_modal = format_unsteady_aero_matrix(force_dof_map, nodes)
    return Q_modal


# start by guessing with natural frequency of mode
def frequency_match(omega_guess, mode_shape, nodes, cquad4_panels, KGG_modal, MGG_modal, omega_pcnt_conv, max_iter):
            
    omega_percent_difference = 1

    iter = 0
    while iter <= max_iter:

        Q_modal = build_unsteady_aero_matrix(omega_guess, mode_shape, nodes, cquad4_panels)

        # Assemble governing eqn: A = -omega^2 M + i*omega Q + K
        A = -omega_guess**2 * MGG_modal + 1j * omega_guess * Q_modal + KGG_modal

        # Solve eigenvalue problem: A * phi = 0
        # Convert to standard eigenproblem (e.g., generalized form: A * x = lambda * B * x)
        # To keep things simple, here we just solve A * phi = 0
        # We'll look for eigenvalues of the matrix pencil:
        # A phi = lambda phi => eig(A)

        eigvals, eigvecs = eig(A)
        idx = np.argmin(np.abs(eigvals))  # choose mode with eigenvalue closest to 0
        phi = eigvecs[:, idx]

        # Compute new omega from Rayleigh quotient
        omega_new = np.sqrt(np.real(np.dot(phi.conj().T, KGG_modal @ phi)) /
                            np.real(np.dot(phi.conj().T, MGG_modal @ phi)))

        # Check convergence
        omega_percent_difference = abs((omega_new - omega_guess) / omega_guess)
        #print(f"Iter {i}: omega = {omega_guess:.4f}, omega_new = {omega_new:.4f}, %diff = {omega_percent_difference*100:.2f}%")

        if omega_percent_difference < omega_pcnt_conv:
            return omega_new, phi

        omega_guess = omega_new
        iter += 1

    raise RuntimeError(f"ERROR: mode shape at {omega_guess} Hz failed to converge. No frequency obtained")
    #TODO: more desc!



