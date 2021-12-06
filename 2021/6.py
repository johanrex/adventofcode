import numpy as np
from timeit import default_timer as timer

def get_initial_state(filename):
    with open(filename) as f:
        line = f.readline()
    lst = line.split(',')

    iarr = np.asarray(lst, np.int64)

    pop_count = np.zeros(9, np.int64)

    unique, counts = np.unique(iarr, return_counts=True)

    for i,_ in enumerate(unique):
        day = unique[i]
        count = counts[i]

        pop_count[day] = count

    return pop_count

def inc_day(pop_count):
    
    #shift everything 1 step to the left
    next = np.append(pop_count[1:], pop_count[0])
    next[6] = next[6] + pop_count[0]

    return next

def challenge(filename, days):
    pop_count = get_initial_state(filename)

    for i in range(days):
        pop_count = inc_day(pop_count)

    print(f'After\t{i+1} days, nr of fish: {pop_count.sum()}')

start = timer()

#part 1
challenge('2021/6_input.txt', 80)

#part 2
challenge('2021/6_input.txt', 256)

print(f'Execution time: {timer() - start}') 
