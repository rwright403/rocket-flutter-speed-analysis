import argparse
import importlib

from src.preprocess.preprocess_openfoam import preprocess_openfoam
from src.preprocess.preprocess_nastran import preprocess_nastran
#from src.sol_flutter.sol_flutter import run_flutter_analysis

def run(input_file):
    #print("\n         			                _______\n	UVic Rocketry Fin Flutter Solver       /       \~\n      				   	      /         \~\n_____________________________________________/           \~\n") #- no figma until it works


    # Dynamically import the input file
    program_input = importlib.import_module(f"src.inputs.{input_file}")

    nas_data = preprocess_nastran(program_input)
    foam_data = preprocess_openfoam(program_input)

