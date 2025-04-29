

from contextlib import contextmanager
import time


### need abstractions for:
"""
- flowfield point:

@dataclass
class flowfield_point:
    pos : np.ndarray
    p : float
    rho : float
    Ma : float #prefer a
    u : np.ndarray

- modal results 
???

- is pynastran .BDF abstraction "nice" for what we are doing here? rn i dont think so but need to do more learning


"""
def _print_stars():
    print("\n" + "*" * 20 + "\n")

def _print_figma():
    print("\n         			                _______\n	UVic Rocketry Fin Flutter Solver       /       \~\n      				   	      /         \~\n_____________________________________________/           \~\n") #- no figma until it works


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