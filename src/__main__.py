import argparse
from src.utils import utils
from src.preprocess import preprocess #TODO:
from src.pk_flutter_sol import pk_flutter_sol
from src.postprocess import postprocess

if __name__ == "__main__":
    # Parse command-line arguments
    
    parser = argparse.ArgumentParser(description='Run the simulation with a specified input file.')
    parser.add_argument('input_file', type=str, help='The name of the input file to use (e.g., constants1) without the .py extension')
    
    args = parser.parse_args()
    
    # Run the program with the specified input file

    ### Preprocess nastran
    input_dat = preprocess.preprocess(args.input_file)

    ### P-K Method to sol flutter: 
    sol = pk_flutter_sol.pk_flutter_sol(input_dat, args.input_file.max_iter, args.input_file.omega_pcnt_conv )
    freestream_speeds, omegas = sol.run()



    ### Postprocessing
    postprocess.root_locus_plot(freestream_speeds, omegas)
    postprocess.write_flutter_results_to_csv(freestream_speeds, omegas, args.input_file.output_filename)