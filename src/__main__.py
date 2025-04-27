import argparse

from src import app

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Run the simulation with a specified input file.')
    parser.add_argument('input_file', type=str, help='The name of the input file to use (e.g., constants1) without the .py extension')
    
    args = parser.parse_args()
    
    # Run the program with the specified input file
    app.run(args.input_file)