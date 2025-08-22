import argparse
import importlib
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
    program_input = importlib.import_module(f"src.inputs.{input_module.input_file}")

    ### Preprocess NASTRAN and CFD
    struct_harmonics = preprocess.read_nastran(program_input)

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


    cfd_cases = preprocess.read_cfd(program_input)

    ## get modal KGG AND MGG

    KGG_modal = struct_harmonics.phi.T @ struct_harmonics.KGG @ struct_harmonics.phi
    MGG_modal = struct_harmonics.phi.T @ struct_harmonics.MGG @ struct_harmonics.phi

    ### State Space method to sol Flutter: 

    collector = dat.FlutterResultsCollector() #initialize pd dataframe collector

    for case in cfd_cases:

        nodes = utils.build_node_plus_dict(struct_harmonics.model, case)
        fin_const_thickness = utils.get_fin_const_thickness(struct_harmonics.model)
        cquad4_panels = utils.build_cquad4_panel_array(fin_const_thickness, struct_harmonics.model.elements, nodes)

        a_free = case.V_free / case.Mach_free

        print("\nBuilding Aero Stiffness Matrix:")
        A_star = aero_model.build_aero_matrix(cquad4_panels, struct_harmonics.phi, struct_harmonics.DOF, aero_model.local_piston_theory_disp)
        
        print("\nBuilding Aero Damping Matrix:")
        B_star = aero_model.build_aero_matrix(cquad4_panels, struct_harmonics.phi, struct_harmonics.DOF, aero_model.local_piston_theory_velo)

        # Sweep speeds
        for V_sweep in program_input.sweep_velocities:

            #note these are modal matrices!
            A =  case.rho_free * a_free * V_sweep * A_star
            B =  case.rho_free * a_free * B_star

            #spin yo block!
            C = np.block([
                [np.zeros((struct_harmonics.phi.shape[1], struct_harmonics.phi.shape[1])), np.eye(struct_harmonics.phi.shape[1])],
                [np.linalg.solve(MGG_modal, A - KGG_modal), np.linalg.solve(MGG_modal, B)],
            ])

            # solve eqn: z_hat * [C] = lambda * z_hat
            eigvals, eigvecs = np.linalg.eig(C)

            # Add case results
            collector.add_case(V_sweep, case, eigvals)

    utils._print_figma()

    ### Postprocessing 
    df = collector.to_dataframe()
    collector.save_csv("flutter_results.csv")
    postprocess.root_locus_plot(df)
    postprocess.v_f_v_g_plot(df)