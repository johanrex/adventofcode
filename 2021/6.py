import numpy as np
from timeit import default_timer as timer

def get_input_array(filename):
    with open(filename) as f:
        line = f.readline()
    lst = line.split(',')
    lst = list(map(int, lst))
    arr = np.asarray(lst)
    return arr

def inc_day(current_arr):
    next_arr = current_arr - 1
    
    count_new = (next_arr == -1).sum()

    next_arr = np.where(next_arr == -1, 6, next_arr)
    next_arr = np.append(next_arr, np.full(count_new, 8) )

    return next_arr


def challenge(filename):
    arr = get_input_array(filename)

    for i in range(256):
        arr = inc_day(arr)
        #print(f'Day {i+1}: {arr}')

    print(f'Nr of fish: {len(arr)}')
    i = 0


challenge('2021/6_input.txt')
