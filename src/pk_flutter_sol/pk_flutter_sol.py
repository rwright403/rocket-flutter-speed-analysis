import numpy as np
from numpy.linalg import eig

class pk_flutter_sol:
    def __init__(self, Mgg_modal, Kgg_modal, max_iter, omega_pcnt_conv):

        self.Mgg_modal = Mgg_modal
        self.Kgg_modal = Kgg_modal

        self.max_iter = max_iter
        self.omega_pcnt_conv = omega_pcnt_conv


        ### on init we want to maybe take parsed data and put them in datastructures!!!

        ### also setup flow vectors and that stuff



    def format_unsteady_aero_matrix(self, Q_phys_unordered, phi):

        ### REORDER DOFS TO MATCH NASTRAN DOF
        Q_phys = 1


        ### TRANSFORM AERO MATRIX TO MODAL SPACE
        Q_modal = phi.T @ Q_phys @ phi
        return Q_modal

    ### BUILD AERO MATRIX IN FREQUENCY DOMAIN AND PHYSICAL SPACE
    def build_unsteady_aero_matrix(self, omega_guess):

        Q_phys_unordered = 1
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

            # Assemble A = -omega^2 M + i*omega Q + K
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

        raise RuntimeError("P–K flutter iteration did not converge.")
        #TODO: more desc!


    ### P-K Method to sol flutter: 
    def run(self):
        omegas = []
          
        for flow_velocity in flow_velocities:

            for mode in noteworthy_modes:
                 
                omegas.append(self.frequency_match(omega_natural_frequency))

        return flow_velocities, omegas
