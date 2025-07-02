import argparse
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
    noteworthy_modes = preprocess.compile_noteworthy_modes(input_module.f_min, input_module.f_max, struct_harmonics.results)

    

    ### P-K Method to sol flutter: 
    freestream_speeds = []
    omegas = []

    for freestream_speed, openfoam_data in openfoam_cases.items():

        nodes = aero_model.build_node_plus_dict(openfoam_data) #NOTE: THIS DOES NOT WORK, BECAUSE 2 FLOWFIELD POINTS UNLESS DOUBLE NODES AND DEAL WITH IN LOCAL PISTON THEORY
        cquad4_panels = aero_model.build_cquad4_panel_array(openfoam_data, nodes)


        for nat_freq, mode in noteworthy_modes.items(): # this should be a dict with key as natural frequency - NOTE: need to build based on input range of natural frequencies to check
            try: 
                omega = aero_model.frequency_match(nat_freq)
                freestream_speeds.append(omega)
                omegas.append(omega)
            except RuntimeError: 
                print(f"ERROR: mode shape at {nat_freq} Hz failed to converge. No frequency obtained")



    ### Postprocessing
    postprocess.root_locus_plot(freestream_speeds, omegas)
    postprocess.write_flutter_results_to_csv(freestream_speeds, omegas, input_module.output_filename)