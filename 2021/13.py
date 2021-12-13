import numpy as np
from pprint import pprint
from timeit import default_timer as timer
t1 = timer()

#filename = '2021/13_input_example.txt'
filename = '2021/13_input.txt'

def flip(m, axis, fold_index):
    if axis == 0:
        a = m[0:fold_index]
        b = m[fold_index+1:(fold_index*2)+1]
    else:
        pass
        a = m[:,0:fold_index]
        b = m[:,fold_index+1:(fold_index*2)+1]

    m = a | np.flip(b, axis)

    return m

def print_matrix(m):
    p = np.full(m.shape, '.')
    p[m==1] = '#'
    for row in p:
        print(''.join(list(row)))

instructions = []
m = np.zeros([2000,2000], np.int8)

#read input
with(open(filename, "r")) as f:
    for line in f:
        line = line.strip()
        if len(line) == 0:
            continue

        if line.startswith('fold'):
            fold_index = int(line[13:])
            axis = 1 if line[11] == 'x' else 0

            instructions.append( (fold_index, axis) )
        else:
            coord = line.split(',')
            m[int(coord[1]), int(coord[0])] = 1

#resize matrix for convenient 
max_fold_row = max([fold_index for fold_index, axis in instructions if axis == 0])
max_fold_col = max([fold_index for fold_index, axis in instructions if axis == 1])

m = m[0:1+max_fold_row*2, 0:1+max_fold_col*2]

# print('Initial state. Shape:', m.shape)
# print_matrix(m)

for i, instruction in enumerate(instructions):
    fold_index, axis = instruction
    m = flip(m, axis, fold_index)

    # print('After:', i+1, 'Shape:',m.shape)
    # print_matrix(m)

    if i == 0:
        print('Part 1. Sum: ', m.sum())

print('After:', i+1, 'Shape:',m.shape)
print_matrix(m)

#HLBUBGFR

t2 = timer()
print(f'time: {(t2-t1):.4f}s')
