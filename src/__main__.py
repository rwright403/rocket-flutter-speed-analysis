import argparse
import numpy as np
from src.utils import utils, dat
from src.preprocess import preprocess
from src.solve import aero_model
from src.postprocess import postprocess

if __name__ == "__main__":
    utils._print_figma()
    # Parse command-line arguments
    
    parser = argparse.ArgumentParser(description='Run the simulation with a specified input file.')
    parser.add_argument('input_file', type=str, help='The name of the input file to use (e.g., constants1) without the .py extension')
    input_module = parser.parse_args()

    ### Preprocess NASTRAN and CFD
    struct_harmonics = preprocess.read_nastran(input_module)

    """
    def find_nodes_with_missing_dofs(grid_to_dof_mapping_mat):
        node_ids = np.unique(grid_to_dof_mapping_mat[0, :])
        missing = {}
        for nid in node_ids:
            dofs = grid_to_dof_mapping_mat[1, grid_to_dof_mapping_mat[0, :] == nid]
            if len(dofs) < 6:
                missing[nid] = dofs.tolist()
        return missing


    print(find_nodes_with_missing_dofs(struct_harmonics.DOF) )"""


    cfd_cases = preprocess.read_cfd(input_module)

    ## get modal KGG AND MGG

    print("KGG shape:", struct_harmonics.KGG.shape)
    print("phi shape:", struct_harmonics.phi.shape)


    KGG_modal = struct_harmonics.phi.T @ struct_harmonics.KGG @ struct_harmonics.phi
    MGG_modal = struct_harmonics.phi.T @ struct_harmonics.MGG @ struct_harmonics.phi


    ### State Space method to sol Flutter: 

    collector = dat.FlutterResultsCollector() #initialize pd dataframe collector

    for case in cfd_cases:

        nodes = aero_model.build_node_plus_dict(struct_harmonics.model, case)

        fin_const_thickness = utils.get_fin_const_thickness(struct_harmonics.model)

        cquad4_panels = aero_model.build_cquad4_panel_array(fin_const_thickness, struct_harmonics.model.elements, nodes)

        #note these are modal matrices!
        A = (case.rho_free * case.V_free**2 / case.Mach_free) * aero_model.build_aero_matrix(
            cquad4_panels, struct_harmonics.phi, struct_harmonics.DOF,
            aero_model.local_piston_theory_disp
        )

        B = (case.rho_free * case.V_free / case.Mach_free) * aero_model.build_aero_matrix(
            cquad4_panels, struct_harmonics.phi, struct_harmonics.DOF,
            aero_model.local_piston_theory_velo
        )

        #spin yo block!
        C = np.block([
            [np.zeros((struct_harmonics.phi.shape[1], struct_harmonics.phi.shape[1])), np.eye(struct_harmonics.phi.shape[1])],
            [np.linalg.solve(MGG_modal, A - KGG_modal), np.linalg.solve(MGG_modal, B)],
        ])

        # solve eqn: z_hat * [C] = lambda * z_hat
        eigvals, eigvecs = np.linalg.eig(C)

        # Add case results
        collector.add_case(case=case, eigvals=eigvals)
       

    ### Postprocessing 
    df = collector.to_dataframe()
    collector.save_csv("flutter_results.csv")
    postprocess.root_locus_plot(df)
    #postprocess.v_f_v_g_plot(df)