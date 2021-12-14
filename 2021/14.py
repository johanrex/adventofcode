import string
from datetime import datetime
from collections import Counter
from functools import lru_cache

from timeit import default_timer as timer
t1 = timer()

filename = '2021/14_input.txt'
#filename = '2021/14_input_example.txt'

polymer_template = []
pair_insertion_rules = {}

def polymerize(target_depth):
    depth = 0

    sum = Counter(polymer_template)

    for i in range(len(polymer_template)-1):
        pair = polymer_template[i:i+2]
        pair = pair[0]+pair[1]

        sum += __polymerize(pair, depth, target_depth)

    diff = max(sum.values()) - min(sum.values())

    return diff


@lru_cache(maxsize=None)
def __polymerize(pair, depth, target_depth):

    depth += 1

    e = pair_insertion_rules[pair]

    if depth == target_depth:
        return Counter([e])
    else:
        left = pair[0] + e
        right = e + pair[1]
        sum = __polymerize(left, depth, target_depth) + __polymerize(right, depth, target_depth) + Counter([e])
        return sum

with(open(filename, "r")) as f:
    for line in f:
        line = line.strip()
        if len(line) == 0:
            continue
        elif len(line) == 7:
            a = line[0:2]
            b = line[6:]

            pair_insertion_rules[a] = b
        else:
            polymer_template = list(line)

print('Starting at:', datetime.now())

#print('Difference:', polymerize(2))
print('Part 1. Difference:', polymerize(10))
print('Part 2. Difference:', polymerize(40))


t2 = timer()
print(f'time: {(t2-t1):.4f}s')
