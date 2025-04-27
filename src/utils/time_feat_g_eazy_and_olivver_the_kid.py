""" 
banger: https://soundcloud.com/skizzymars/time
also the code is below:
"""

from contextlib import contextmanager
import time

@contextmanager
def runtime(name="Block"):
    print(f"[{name} - starting]")
    start = time.time()
    yield
    end = time.time()
    print(f"[{name}] - finished, elapsed {end - start:.3f} seconds")