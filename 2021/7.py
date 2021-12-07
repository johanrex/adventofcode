import common
from typing import List
import numpy as np

def part1_cost(arr):
    median = int(np.median(arr))
    result = np.absolute(arr - median).sum()
    return result

def align_cost(arr, align_pos):
    steps =  np.absolute(arr - align_pos)

    cost_of_steps = (steps * (steps + 1))/2
    cost_of_steps = cost_of_steps.astype(np.int64)

    return cost_of_steps.sum()

@common.timed
def challenge(filename):
    arr = common.read_file_as_int_array(filename)
    arr = np.sort(arr)

    result = part1_cost(arr)
    print(f'Part 1. Sum of fuel: {result}.')

    mean = int(np.mean(arr))
    
    costs = []
    align_position_candidates = [mean-1, mean, mean+1]
    for pos in align_position_candidates:
        costs.append(align_cost(arr, pos))

    cost = min(costs)

    print(f'Part 2. Sum of fuel: {cost}.')    

#challenge('2021/7_input_example.txt')
challenge('2021/7_input.txt')