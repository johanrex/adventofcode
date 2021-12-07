from typing import List
from timeit import default_timer as timer
import numpy as np

def read_file(filename: str) -> List[str]:

    with(open(filename, "r")) as f:
        s = f.read().splitlines()

    return s

def timed(func):
    def wrap_func(*args, **kwargs):
        t1 = timer()
        result = func(*args, **kwargs)
        t2 = timer()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')
        return result
    return wrap_func

def read_file_as_int_array(filename: str) -> List[int]:
    with open(filename) as f: 
        line = f.readline()

    values = line.strip().split(',')

    return np.asarray(values, np.int64)
