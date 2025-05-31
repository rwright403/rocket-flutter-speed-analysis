import time
from contextlib import contextmanager

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

"""
def trans_matrix_phys_to_modal(phi,A):
    return phi.T @ A @ phi