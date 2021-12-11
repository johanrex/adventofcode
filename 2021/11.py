import numpy as np
from timeit import default_timer as timer
t1 = timer()

def read_input(filename):
    inputs = []
    with(open(filename, "r")) as f:
        for line in f:
            row = list(line.strip())
            inputs.append(row)

    m = np.asarray(inputs, np.int8)
    return m

def print_mtx(m):
    m = m.astype(str)
    for row in m:
        print(''.join(row))

def flash(m):

    flashers = np.where(m >= 10)
    m[m >= 10] = 0

    global nr_of_flashes
    nr_of_flashes += len(flashers[0])

    points_affected = []

    for row,col in zip(flashers[0], flashers[1]):

        for pt in (
            (row-1, col-1),
            (row-1, col),
            (row-1, col+1),
            (row, col-1),
            (row, col+1),
            (row+1, col-1),
            (row+1, col),
            (row+1, col+1)
        ):
            #Skip points outside matrix and those already flashed.             
            if (
                (0 <= pt[0] < m.shape[0]) and 
                (0 <= pt[1] < m.shape[1]) and 
                (m[pt[0], pt[1]] != 0)
            ):
                #+1 for all affected
                m[ pt[0], pt[1] ] = m[ pt[0], pt[1] ] + 1
    
    if np.any(m >= 10):
        flash(m)

filename = '2021/11_input.txt'
m = read_input(filename)

part1_nr_of_flashes = 0
nr_of_flashes = 0
step_when_all_flash = 0

# print('Before any steps:')
# print_mtx(m)
# print('')

#Steps
for i in range(1000):
    step = i+1
    m = m + 1

    flash(m)
    if step == 100:
        part1_nr_of_flashes = nr_of_flashes

    if not np.any(m > 0):
        step_when_all_flash = step
        break

    # print(f'After step {step}:')
    # print_mtx(m)
    # print('')
i = 0

print(f'Part 1. Nr of flashes: {part1_nr_of_flashes}')
print(f'Part 2. step_when_all_flash ', step_when_all_flash)

t2 = timer()
print(f'time: {(t2-t1):.4f}s')
