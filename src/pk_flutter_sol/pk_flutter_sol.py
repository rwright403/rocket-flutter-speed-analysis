import numpy as np
from numpy.linalg import eig
from src.utils import utils

class pk_flutter_sol:
    def __init__(self, input_dat, max_iter, omega_pcnt_conv):

        self.input_dat = input_dat

        self.freestream_speeds = self.input_dat.freestream_speeds

        self.cquad_4_elements = input_dat.cquad_4_elements
        self.noteworthy_modes = 1 #TODO:

        self.Mgg_modal = input_dat.Mgg_modal
        self.Kgg_modal = input_dat.Kgg_modal

        self.max_iter = max_iter
        self.omega_pcnt_conv = omega_pcnt_conv





    ### 

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

        #Q_phys_unordered = np.array([]) convert to np array
        phi = 1

        Q_modal = self.format_unsteady_aero_matrix(Q_phys_unordered, phi)
        return Q_modal








    def frequency_match(self, omega_natural_frequency):
                
        # start by guessing with natural frequency of mode
        omega_guess = omega_natural_frequency
        omega_percent_difference = 1

        iter = 0
        while iter  <= self.max_iter:

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

        raise RuntimeError("P-K flutter iteration did not converge.")
        #TODO: more desc!


    ### P-K Method to sol flutter: 
    def run(self):
        omegas = []
          
        #TODO: extract freestream speeds!
        for freestream_vel in self.freestream_speeds:

            #TODO: PASS IN FREESTREAM VELOCITY AS KEY TO FIND THE CFD CASE VAL!!!!
            self.input_dat.build_node_plus_dict(freestream_vel)
            self.input_dat.build_cquad4_panel_array(freestream_vel)

            for nat_freq, mode in self.noteworthy_modes.items(): # this should be a dict with key as natural frequency
                 
                omegas.append( self.frequency_match(nat_freq) )

        return omegas
