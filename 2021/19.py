import numpy as np
import pandas as pd
import itertools

def parse_input(filename):
    with open(filename, 'r') as f:

        scanners = []
        current_scanner = None
        for line in f:

            line = line.strip()

            if line.startswith('---'):

                current_scanner = []
                scanners.append(current_scanner)

            elif len(line) == 0:

                continue

            else:

                vals = list(map(int, line.split(',')))
                current_scanner.append(vals)

    #Add a line to the scanners that only have 25 readings. 
    # missing_measure_scanners = [scanner for scanner in scanners if len(scanner) != 26]
    # for missing_measure_scanner in missing_measure_scanners:
    #     missing_measure_scanner.append([np.NaN, np.NaN, np.NaN])

    #All scanners should have 26 readings goddamnit. 
    # if any( (scanner for scanner in scanners if len(scanner) != 26) ):
    #     raise Exception("ffs")

    return [np.asarray(scanner) for scanner in scanners]

def get_rotation(m):
    
    permutations = list(itertools.permutations([0, 1, 2]))
    for perm in permutations:
        x,y,z = perm

        #permutations
        p = m[:, [x,y,z]]

        #normal rotation
        yield p

        #inplace multiply first and second columns with -1
        p[:,[0,1]] *= -1
        yield p
        
        tmp1 = p[:,[1, 0, 2]] #swap first and second column
        tmp1[:,[0]] *= -1 #switch sign on first column. 
        yield tmp1

        tmp2 = p[:,[1, 0, 2]] #swap first and second column
        tmp2[:,[1]] *= -1 #switch sign on second column. 
        yield tmp2


def has_matching_beacons(a, b):
    dfa = pd.DataFrame(a)
    dfb = pd.DataFrame(b)

    matches = pd.merge(dfa, dfb, on=[0, 1, 2])

    return matches.shape[0] >= 12


#filename = '2021/19_input_example.txt'
filename = '2021/19_input.txt'
input = parse_input(filename)


#In total, each scanner could be in any of 24 different orientations: facing positive or negative x, y, or z, and considering any of four directions "up" from that facing.
#By finding pairs of scanners that both see at least 12 of the same beacons, you can assemble the entire map. 


pairs_matched = []

for i in range(len(input)):
    first = input[i]
    for j in range(len(input)):
        if i == j:
            continue

        print(f'Testing {i} and {j}.')

        matched = False

        for pair in pairs_matched:
            if (
                i == pair[0] or i == pair[1] or
                j == pair[0] or j == pair[1]
            ):
                matched = True
                break

        second = input[j]

        for p in get_rotation(second):

            #TODO translations....

            match = has_matching_beacons(first, p)

            if match:
                pairs_matched.append( (i, j) )
                matched = True
                break
        
        if matched:
            break

i = 0