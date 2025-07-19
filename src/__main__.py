import argparse
import numpy as np
import pandas as pd
from src.utils import utils
from src.preprocess import preprocess
from solve import aero_model, struct
from src.postprocess import postprocess

if __name__ == "__main__":
    utils._print_figma()
    # Parse command-line arguments
    
    parser = argparse.ArgumentParser(description='Run the simulation with a specified input file.')
    parser.add_argument('input_file', type=str, help='The name of the input file to use (e.g., constants1) without the .py extension')
    
    input_module = parser.parse_args()

    ### Preprocess NASTRAN and OpenFOAM
    struct_harmonics = preprocess.read_nastran(input_module)
    openfoam_cases = preprocess.read_openfoam(input_module)

    ### Initialize Dataframe

    #TODO:

    #TODO:
    elastic_axis = struct.solve_elastic_axis_isotropic_fin()
    #NOTE: bending_axis for a symmetrical fin on xz plane --> moment arm is just 1/2*t

    ## get modal KGG AND MGG
    KGG_modal = utils.trans_matrix_phys_to_modal(struct_harmonics.phi, struct_harmonics.KGG)
    MGG_modal = utils.trans_matrix_phys_to_modal(struct_harmonics.phi, struct_harmonics.MGG)

    ### State Space method to sol Flutter: 

    # i think i need to expand "freestream speed" to freestream conditions
    for freestream_speed, openfoam_data in openfoam_cases.items():

        nodes = aero_model.build_node_plus_dict(openfoam_data)
        cquad4_panels = aero_model.build_cquad4_panel_array(struct_harmonics.model.elements, nodes)
        

        A = (rho_frestream * V**2 / Ma_ref) * aero_model.build_aero_matrix(struct_harmonics.n_modes, nodes, cquad4_panels, struct_harmonics.phi, aero_model.local_piston_theory_disp)
        B = (rho * V / Ma_ref) * aero_model.build_aero_matrix(struct_harmonics.n_modes, nodes, cquad4_panels, struct_harmonics.phi, aero_model.local_piston_theory_velo)

        C = np.block([
            [np.zeros((struct_harmonics.n_modes, struct_harmonics.n_modes)), np.eye(struct_harmonics.n_modes)],
            [np.linalg.solve(MGG_modal, A - KGG_modal), np.linalg.solve(MGG_modal, B),]

        ])

        # solve eqn: z_hat * [C] = lambda * z_hat
        eigvals, _ = np.linalg.eig(C)


    ### TODO: CREATE LISTS!!!
       

    ### Postprocessing 

    #redo this, we are getting a series of eigenvalues per flight speed
    postprocess.root_locus_plot("""redo this function to take in pandas dataframe)