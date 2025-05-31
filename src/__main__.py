import argparse
from . import utils
from preprocess.preprocess_nastran import preprocess_nastran  #TODO:
from preprocess.preprocess_openfoam import preprocess_openfoam  #TODO:
from pk_flutter_sol.pk_flutter_sol import pk_flutter_sol
from postprocess.postprocess import root_locus_plot, write_flutter_results_to_csv

if __name__ == "__main__":
    # Parse command-line arguments
    
    parser = argparse.ArgumentParser(description='Run the simulation with a specified input file.')
    parser.add_argument('input_file', type=str, help='The name of the input file to use (e.g., constants1) without the .py extension')
    
    args = parser.parse_args()
    
    # Run the program with the specified input file

    ### Preprocess nastran


    ### P-K Method to sol flutter: 
    sol = pk_flutter_sol(1, 1, args.input_file.max_iter, args.input_file.omega_pcnt_conv )
    flow_velocities, omegas = sol.run()



    ### Postprocessing
    root_locus_plot(flow_velocities, omegas)
    write_flutter_results_to_csv(flow_velocities, omegas, "out.csv") #TODO:
    