import time
from contextlib import contextmanager
import numpy as np
from scipy.sparse import csr_matrix
import re

def _print_stars():
    print("\n" + "*" * 20 + "\n")

def _print_figma():
    print(r"\n         			                _______\n	UVic Rocketry Fin Flutter Solver       /       \~\n      				   	      /         \~\n_____________________________________________/           \~\n") #- no figma until it works


""" 
runtime
Record and print the runtime of a section of code
"""
@contextmanager
def runtime(name="Block"):
    print(f"[{name} - starting]")
    start = time.time()
    yield
    end = time.time()
    print(f"[{name}] - finished, elapsed {end - start:.3f} seconds")


"""
given a string of the desired matrix and the filepath to a sparse .mat file, read it into python and return a scipy .csr matrix
"""
def read_and_parse_mat_file(mat_str, filepath):
    
    with open(filepath, 'r') as f:
        lines = f.readlines()

    # Find the start of the desired matrix block
    row_idx = None
    for idx, line in enumerate(lines):
        if line.strip().startswith(mat_str):
            row_idx = idx
            break

    print(f"\nthe row found is {row_idx}\n")

    # Parse header line
    header = lines[row_idx].split()

    data = []
    data_row_idx = []
    data_col_idx = []

    shape = ( int(header[4]), int(header[5]) )

    if int(header[3]) == 1:
        raise NotImplementedError("Dense Matrix read/process not implemented yet, add 'OUTPUT,MATRIX,FULL,SPARSE' to hypermesh .fem file before case ctrl.")

    row_idx += 1

    while list(map(int, lines[row_idx].strip().split()))[0] != 0:

        # Parse the index row
        index_parts = list(map(int, lines[row_idx].strip().split()))
        col = index_parts[0]
        row1 = index_parts[1]
        row2 = index_parts[2]
        row_idx += 1

        # Parse the data row
        #data_parts = list(map(float, lines[row_idx].strip().split()))
        ### above does not work because of edge case: ValueError: could not convert string to float: '8.348207789E+07-1.040078924E+05'
        data_parts = list(map(float, re.findall(r'[+-]?\d+\.\d+(?:[Ee][+-]?\d+)?', lines[row_idx].strip())))

        #NOTE: -1 to convert from .mat 1-based idx to py 0-based idx
        data_col_idx.append(col - 1)
        data_row_idx.append(row1 - 1)
        
        #print(data_parts[0])

        data.append(data_parts[0])

        if row1 != row2:
            data_col_idx.append(col - 1)
            data_row_idx.append(row2 - 1)
            data.append(data_parts[1])
        row_idx += 1


    return csr_matrix((data, ( np.array(data_row_idx), np.array(data_col_idx) )), shape=shape)





"""
given the mode shape matrix and a global matrix, return the global matrix in modal coords
"""
def trans_matrix_phys_to_modal(phi,A):

    print("phi shape:", phi.shape)
    print("A shape:", A.shape)
    print("T @ A shape:",  phi.T @ A)

    return phi.T @ A @ phi