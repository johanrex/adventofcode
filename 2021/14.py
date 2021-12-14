
import re
import numpy

filename = '2021/14_input.txt'
#filename = '2021/14_input_example.txt'

polymer_template = []
pair_insertion_rules = {}

def step():
    for i in range(len(polymer_template)-2, -1, -1):
        pair = polymer_template[i:i+2]
        pair = pair[0]+pair[1]

        element_to_insert = pair_insertion_rules[pair]
        polymer_template.insert(i+1, element_to_insert)

def difference():
    a = numpy.array(polymer_template)
    unique, counts = numpy.unique(a, return_counts=True)
    return counts.max() - counts.min()

with(open(filename, "r")) as f:
    for line in f:
        line = line.strip()
        if len(line) == 0:
            continue
        elif len(line) == 7:
            a = line[0:2]
            b = line[6:]

            if a not in pair_insertion_rules:
                pair_insertion_rules[a] = b
            else:
                raise Exception('weird')

        else:
            polymer_template = list(line)


for i in range(40):
    print('step', i+1)
    step()
    #print(''.join(polymer_template))


    if i == 9:
        part_1 = difference()


part_2 = difference()

print('Part 1. Difference:', part_1)
print('Part 2. Difference:', part_2)

i = 0
