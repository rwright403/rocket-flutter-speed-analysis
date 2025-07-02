import numpy as np
from numpy.linalg import eig
from src.utils import utils, dat

"""
Parse the openfoam data and build all the node+ objects
"""
def build_node_plus_dict(self, openfoam_data):

    node_ids = sorted(self.model.nodes.keys())
    coords = np.array([self.model.nodes[nid].xyz for nid in node_ids])

    nodes = {}
    # Build list of node_plus instances
    for i, nid in enumerate(node_ids):

        nodes[nid] = dat.node_plus(
            r_=coords[nid],
            p=(openfoam_data.pressures[i]),
            rho=(openfoam_data.densities[i]),
            a=np.sqrt(dat.GAMMA*openfoam_data.temperatures[i]*dat.R_SPEC_AIR),
            u_= openfoam_data.velocites[i],
        )
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
def local_piston_theory(node, n_, omega):

    delta_n_ = 1

    u_b_ = omega * 1j #NOTE: WHAT IS q_hat!!!

    w_ = u_*delta_n_ + u_b_*n_ # type: ignore

    return node.p + node.rho*node.a *w_ # type: ignore


"""
loop through all nodes and solve the force of lift contribution from each panel
don't return anything, just update the nodes - makes it easy to then build the aero matrix!
"""
def solve_aero_force(nodes, cquad4_panels, omega):
    
    for cquad4_panel in cquad4_panels:

        cquad4_panel.n_
        for node in cquad4_panel:
            p_unst = local_piston_theory(node, cquad4_panel.n_, omega)

            dF_panel = -p_unst*cquad4_panel.n_*cquad4_panel.jacobian
            
            ### put node shape function in node+ ?
            # F on node += node.shape_func + dF_panel

        
    x=1














def format_unsteady_aero_matrix(self, Q_phys_unordered, phi):

    ### REORDER DOFS TO MATCH NASTRAN DOF
    Q_phys = 1


    ### TRANSFORM AERO MATRIX TO MODAL SPACE
    Q_modal = utils.trans_matrix_phys_to_modal(phi, Q_phys)
    return Q_modal




### BUILD AERO MATRIX IN FREQUENCY DOMAIN AND PHYSICAL SPACE
def build_unsteady_aero_matrix(self, omega_guess):

    Q_phys_unordered = []

    """
    for every aero panel:
        for every node in aero panel
            call the local piston theory on every node in the aero panel to get unsteady pressure


            jacobian = panel.compute_jacobian() #solve jacobian per panel
            df = -p_param * panel.n_*jacobian # solve dF of node

            -numerically integrate force per node --> 
            -add panel contribution to the total force on the node


    for every node: 
        Q_phys_unordered.append(aero_force_on_node_from_panel) #append force per node to Q_phys_unordered!

    """
    #NO: NOT THIS SIMPLE, NEED TO KNOW TORISIONAL AND FLEXURAL AXIS and solve moment
####
###
##
#

    #Q_phys_unordered = np.array([]) convert to np array
    phi = 1

    Q_modal = self.format_unsteady_aero_matrix(Q_phys_unordered, phi)
    return Q_modal



def frequency_match(self, omega_natural_frequency):
            
    # start by guessing with natural frequency of mode
    omega_guess = omega_natural_frequency
    omega_percent_difference = 1

    iter = 0
    while iter <= self.max_iter:

        Q = self.build_unsteady_aero_matrix(omega_guess)

        # Assemble governing eqn: A = -omega^2 M + i*omega Q + K
        A = -omega_guess**2 * self.Mgg_modal + 1j * omega_guess * Q + self.Kgg_modal

        # Solve eigenvalue problem: A * phi = 0
        # Convert to standard eigenproblem (e.g., generalized form: A * x = lambda * B * x)
        # To keep things simple, here we just solve A * phi = 0
        # We'll look for eigenvalues of the matrix pencil:
        # A phi = lambda phi => eig(A)

        eigvals, eigvecs = eig(A)
        idx = np.argmin(np.abs(eigvals))  # choose mode with eigenvalue closest to 0
        phi = eigvecs[:, idx]

        # Compute new omega from Rayleigh quotient
        omega_new = np.sqrt(np.real(np.dot(phi.conj().T, self.Kgg_modal @ phi)) /
                            np.real(np.dot(phi.conj().T, self.Mgg_modal @ phi)))

        # Check convergence
        omega_percent_difference = abs((omega_new - omega_guess) / omega_guess)
        #print(f"Iter {i}: omega = {omega_guess:.4f}, omega_new = {omega_new:.4f}, %diff = {omega_percent_difference*100:.2f}%")

        if omega_percent_difference < self.omega_pcnt_conv:
            return omega_new, phi

        omega_guess = omega_new
        iter += 1

    raise RuntimeError(f"ERROR: mode shape at {omega_natural_frequency} Hz failed to converge. No frequency obtained")
    #TODO: more desc!



