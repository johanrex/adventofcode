import string
from datetime import datetime

from timeit import default_timer as timer
t1 = timer()

filename = '2021/14_input.txt'
#filename = '2021/14_input_example.txt'

polymer_template = []
element_count = {}
pair_insertion_rules = {}

def difference():
    vals = sorted(x for x in element_count.values() if x > 0)
    return vals[len(vals)-1] - vals[0] 

def polymerize(target_depth):
    depth = 0

    for c in polymer_template:
        element_count[c] += 1

    for i in range(len(polymer_template)-1):
        pair = polymer_template[i:i+2]
        pair = pair[0]+pair[1]

        __polymerize(pair, depth, target_depth)
    
        # print(f'Done {((i+1)/len(polymer_template))*100:.2f}%')

    return difference()

def __polymerize(pair, depth, target_depth):

    depth += 1

    e = pair_insertion_rules[pair]
    element_count[e] += 1

    if depth == target_depth:
        return

    __polymerize(pair[0] + e, depth, target_depth)
    __polymerize(e + pair[1], depth, target_depth)


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

#init element count
for c in string.ascii_uppercase:
    element_count[c] = 0

print('Starting at:', datetime.now())
print('Step 10. Difference:', polymerize(10))
#print('Part 2. Difference:', polymerize(40))


t2 = timer()
print(f'time: {(t2-t1):.4f}s')
