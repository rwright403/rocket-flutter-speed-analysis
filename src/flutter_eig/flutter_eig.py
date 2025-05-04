import sympy as sp
import numpy as np


def solve_unsteady_local_downwash_speed_harmonic_vec(U_cfd_vec, norm_vec):

    delta_norm_vec = 1
    v_vibes_vec = 1

    w_vib_vec = np.einsum('ij,ij->i', U_cfd_vec, delta_norm_vec)
    w_vib_vec = w_vib_vec[:, np.newaxis]


    w_def_vec = np.einsum('ij,ij->i', v_vibes_vec, norm_vec)
    w_def_vec = w_def_vec[:, np.newaxis]
    
    w_vec = w_def_vec + w_vib_vec




    return w_vec



# Local Piston Theory vector!!!
def solve_LPT_vec(P_cfd_vec, rho_cfd_vec, a_cfd_vec, U_cfd_vec, norm_vec):

    w_vec = solve_unsteady_local_downwash_speed_harmonic_vec(U_cfd_vec, norm_vec)
    delta_P_vec =  rho_cfd_vec*a_cfd_vec*w_vec

    return delta_P_vec


def build_gen_aero_force_vec():
    F = 0


def build_solve_matrix(V):
    S = 1


"""
given structural and flowfield data where the flowfield has been interpolated onto the structural elements
return the eigenvalue

"""
def flutter_eig(nas_dat, foam_data):

    #given interpolated flowfield onto structural elements

    #for every pressure in flowfield, solve LPT

    # build eqns for matrix S


    #solve matrix [S] given freestream velocity V
    # S = build_solve_matrix(V)
    # eigvals = np.linalg.eigvals(S)
    

    ### output eigenvalue root loci of the matrix [S]
    x = 1


    #return eig, V, Ma