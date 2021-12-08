
import collections
import itertools

DisplayDataInput = collections.namedtuple('DisplayDataInput', ['unique_display_patterns', 'display_values'])
DisplayDataOutput = collections.namedtuple('DisplayDataOutput', ['unmapped_patterns', 'mapped_patterns'])

def read_input(filename):

    inputs = []
    with(open(filename, "r")) as f:
        for line in f:
            first, second = line.split('|')

            inputs.append(
                DisplayDataInput(
                    unique_display_patterns = first.strip().split(),
                    display_values = second.strip().split()
                    )
            )

    return inputs

def pattern_mapper(inputs):
    sum = 0

    """
    Number 1: length: 2 * 
    Number 2: length: 5
    Number 3: length: 5
    Number 4: length: 4 * 
    Number 5: length: 5
    Number 6: length: 6
    Number 7: length: 3 * 
    Number 8: length: 7 * 
    Number 9: length: 6
    Number 0: length: 6
    """

    for input in inputs:

        mapper = {}

        patterns = [''.join(sorted(pat)) for pat in input.unique_display_patterns]

        #Assign 1, 4, 7, 8
        mapper[1] = next(pattern for pattern in patterns if len(pattern) == 2)
        mapper[4] = next(pattern for pattern in patterns if len(pattern) == 4)
        mapper[7] = next(pattern for pattern in patterns if len(pattern) == 3)
        mapper[8] = next(pattern for pattern in patterns if len(pattern) == 7)

        #Find 9
        candidates = [pattern for pattern in patterns if len(pattern) == 6] #9, 0 and 6 has 6 segments. 
        set_almost = set(mapper[4] + mapper[7]) #4 && 7 + one segment can only be 9
        mapper[9] = next(pat for pat in candidates if len(set(pat).difference(set_almost)) == 1)

        #Find 6
        candidates.remove(mapper[9]) #Remove 9 from 6-segment candidates. Now only 6 and 0 remains.
        set_almost = set(mapper[4]).difference(set(mapper[1])) #4 - 1 contains the segments b and d, which can be found in only 0 of the remaining 6-segment candidates. 
        mapper[6] = next(pat for pat in candidates if len(set(pat).difference(set_almost)) == 4)

        #Find 0
        candidates.remove(mapper[6]) #Remove 6. Now only 0 remains of the 6-segment patterns. 
        mapper[0] = candidates[0]

        #Find 3
        candidates = [pattern for pattern in patterns if len(pattern) == 5] # 2, 3 and 5 has 5 segments. 
        set_almost = set(mapper[1]) # pattern for 1 matches part of pattern for 3. 
        mapper[3] = next(pat for pat in candidates if (set(pat) & set_almost) == set_almost)

        #Find 2
        candidates.remove(mapper[3])
        set_almost = set(mapper[8]).difference(set(mapper[6])) # 8 - 6 matches 2, but not 5. 
        mapper[2] = next(pat for pat in candidates if (set(pat) & set_almost) == set_almost)

        #5, the last one. 
        candidates.remove(mapper[2])
        mapper[5] = candidates[0]

        #Let's print out the values. 
        reverse_mapper = {value : key for (key, value) in mapper.items()}

        s = ''
        for val in input.display_values:
            val = ''.join(sorted(val))
            s += str(reverse_mapper[val])
        
        sum += int(s)


    print(f'Part 2. Sum: {sum}.')

inputs = read_input('2021/8_input.txt')

pattern_mapper(inputs)



for display_data_input in inputs:
    parse_sensor(display_data_input)

print(f'Part 1. Sum: {targets}')

# det borde finnas någon av 1,4,7,8 på varje rad..

i = 0