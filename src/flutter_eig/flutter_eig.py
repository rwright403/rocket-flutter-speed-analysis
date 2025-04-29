import sympy as sp

# Local Piston Theory for one point
def solve_lpt(P_surf , rho_surf, a_surf, U_surf, norm):
    
    W = norm #TODO: figure out eqn - makes sense to work in fequency domain from start or convert later?

    P_i = P_surf + rho_surf*a_surf*W


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