import sympy as sp
import numpy as np

def solve_cquad4_centroid():

def solve_cquad4_norm_vec():
    


def solve_unsteady_local_downwash_speed_harmonic(U_cfd, norm):

#TODO: 
    delta_norm = 1
    v_vibes = 1

    w_vib = np.einsum('ij,ij->i', U_cfd, delta_norm)
    w_vib = w_vib[:, np.newaxis]


    w_def = np.einsum('ij,ij->i', v_vibes, norm)
    w_def = w_def[:, np.newaxis]
    
    w = w_def + w_vib


    return w



# Local Piston Theory at a point!!!
def solve_LPT_pt(P_cfd, rho_cfd, a_cfd, U_cfd, norm):

    w = solve_unsteady_local_downwash_speed_harmonic(U_cfd, norm)
    delta_P =  rho_cfd*a_cfd*w

    return delta_P


def build_gen_aero_force():
    F = 0


def build_solve_matrix(V):
    S = 1


"""
given structural and flowfield data where the flowfield has been interpolated onto the centroids of the structural elements
return the eigenvalue

"""
def flutter_eig(nas_dat, foam_data):

    #for every pressure in flowfield, solve LPT

    #interpolate aero onto structural

    # build eqns for matrix S


    #solve matrix [S] given freestream velocity V
    # S = build_solve_matrix(V)
    # eigvals = np.linalg.eigvals(S)
    

    ### output eigenvalue root loci of the matrix [S]
    x = 1


    #return eig, V, Ma