import argparse
import importlib
from src.utils import utils
from src.preprocess.preprocess_openfoam import preprocess_openfoam
from src.preprocess.preprocess_nastran import preprocess_nastran
from src.sol_flutter.sol_flutter import sol_flutter

def postprocess(eig, V, Ma):

    utils._print_stars()
    if eig.real >= 0 and eig.imag != 0:
        print(f"Flutter Possible at V = {V:.2f} m/s (Ma = {Ma})")
    else:
        print(f"Flutter Likely ***not Possible*** at tested point V = {V:.2f} m/s (Ma = {Ma})")
    utils._print_stars()


def run(input_file):
        # Import the input module
    try:
        program_input = importlib.import_module(f"src.inputs.{input_file}")
    except ModuleNotFoundError as e:
        print(f"Error: Module 'src.inputs.{input_file}' not found.")
        raise
    
    # how to abstract these best?
    nas_data = preprocess_nastran(program_input)
    foam_data = preprocess_openfoam(program_input)

    ###
    eig = sol_flutter(nas_data, foam_data)

    postprocess(eig, 1, 1)





