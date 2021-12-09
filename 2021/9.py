import numpy as np
import scipy
from scipy.signal import argrelextrema

def read_input(filename):
    inputs = []
    with(open(filename, "r")) as f:
        for line in f:
            row = list(line.strip())
            inputs.append(row)

    mtx = np.asarray(inputs, np.int8)
    return mtx

#filename = '2021/9_input_example.txt'
filename = '2021/9_input.txt'

mtx = read_input(filename)

#pad with bigger value outside
mtx = np.pad(mtx, 1, constant_values=10)


smallest = []
rows, cols = mtx.shape
for x in range(1, rows-1):
    for y in range(1, cols-1):

        val = mtx[x,y]

        #is smaller than adjacent?
        if (
            val < mtx[x-1,y] and 
            val < mtx[x+1,y] and 
            val < mtx[x,y-1] and 
            val < mtx[x,y+1]
        ):
            smallest.append(val)

sum = (np.array(smallest)+1).sum()
print(f'Part 1. Sum: {sum}.')
