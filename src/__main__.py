import argparse
import numpy as np
import pandas as pd
from src.utils import utils, dat
from src.preprocess import preprocess
from solve import aero_model, struct
from src.postprocess import postprocess

if __name__ == "__main__":
    utils._print_figma()
    # Parse command-line arguments
    
    parser = argparse.ArgumentParser(description='Run the simulation with a specified input file.')
    parser.add_argument('input_file', type=str, help='The name of the input file to use (e.g., constants1) without the .py extension')
    input_module = parser.parse_args()

    ### Preprocess NASTRAN and CFD
    struct_harmonics = preprocess.read_nastran(input_module)
    cfd_cases = preprocess.read_cfd(input_module)


#TODO:
    elastic_axis = struct.solve_elastic_axis_isotropic_fin()
    #NOTE: bending_axis for a symmetrical fin on xz plane --> moment arm is just 1/2*t

    ## get modal KGG AND MGG
    KGG_modal = utils.trans_matrix_phys_to_modal(struct_harmonics.phi, struct_harmonics.KGG)
    MGG_modal = utils.trans_matrix_phys_to_modal(struct_harmonics.phi, struct_harmonics.MGG)


    ### State Space method to sol Flutter: 

    collector = dat.FlutterResultsCollector() #initialize pd dataframe collector

    for case in cfd_cases:

        nodes = aero_model.build_node_plus_dict(case)
        cquad4_panels = aero_model.build_cquad4_panel_array(struct_harmonics.model.elements, nodes)

        #note these are modal matrices!
        A = (case.rho * case.V**2 / case.Ma) * aero_model.build_aero_matrix(
            struct_harmonics.n_dofs, nodes, cquad4_panels,
            struct_harmonics.phi, struct_harmonics.DOF,
            aero_model.local_piston_theory_disp
        )

        B = (case.rho * case.V / case.Ma) * aero_model.build_aero_matrix(
            struct_harmonics.n_dofs, nodes, cquad4_panels,
            struct_harmonics.phi, struct_harmonics.DOF,
            aero_model.local_piston_theory_velo
        )

        #spin yo block!
        C = np.block([
            [np.zeros((struct_harmonics.n_modes, struct_harmonics.n_dofs)), np.eye(struct_harmonics.n_dofs)],
            [np.linalg.solve(MGG_modal, A - KGG_modal), np.linalg.solve(MGG_modal, B)],
        ])

        # solve eqn: z_hat * [C] = lambda * z_hat
        eigvals, _ = np.linalg.eig(C)


        # Add case results
        collector.add_case(case=case, eigvals=eigvals)
       

    ### Postprocessing 
    # Postprocessing
    df = collector.to_dataframe()
    collector.save_csv("flutter_results.csv")
    postprocess.root_locus_plot(df) #TODO: REDO THIS TO TAKE IN THE DATAFRAME NOT WHATEVER LEGACY
    postprocess.v_f_v_g_plot(df)