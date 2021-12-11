import numpy as np
from timeit import default_timer as timer
t1 = timer()

def read_input(filename):
    lines = []
    with(open(filename, "r")) as f:
        lines = [ list(line.strip()) for line in f.readlines() ]

    m = np.asarray(lines, np.int8)
    return m

def print_mtx(m):
    m = m.astype(str)
    for row in m:
        print(''.join(row))

def step(m):

    nr_of_flashes = 0
    rolls = []

    #keep track of those that is already zero in this step
    mbz = m==0

    while True:
        mb = m>=10
        mf = mb.astype(np.int8)

        s = mf.sum()

        if s>0:
            nr_of_flashes += s

            #Pad with 0
            mfp = np.pad(mf, pad_width=1, mode='constant', constant_values=0)

            """
            345
            2x6
            107
            """

            rolls.clear()
            rolls.append(np.roll(mfp, 1, 0)) #0
            rolls.append(np.roll(rolls[0], -1, 1)) #1
            rolls.append(np.roll(rolls[1], -1, 0)) #2
            rolls.append(np.roll(rolls[2], -1, 0)) #3
            rolls.append(np.roll(rolls[3], 1, 1)) #4
            rolls.append(np.roll(rolls[4], 1, 1)) #5
            rolls.append(np.roll(rolls[5], 1, 0)) #6
            rolls.append(np.roll(rolls[6], 1, 0)) #7

            madj = \
                rolls[0] + \
                rolls[1] + \
                rolls[2] + \
                rolls[3] + \
                rolls[4] + \
                rolls[5] + \
                rolls[6] + \
                rolls[7]

            #Remove padding
            madj = madj[1:-1, 1:-1]

            m += madj

            mbz |= mb

            #set all flashed to 0
            m[mbz] = 0
           
        else:
            break

    return nr_of_flashes

filename = '2021/11_input.txt'
m = read_input(filename)

part1_nr_of_flashes = 0
nr_of_flashes = 0
step_when_all_flash = 0

# print('Before any steps:')
# print_mtx(m)
# print('')

#Steps
for i in range(500):
    step_nbr = i+1
    m += 1

    nr_of_flashes += step(m)
    if step_nbr == 100:
        part1_nr_of_flashes = nr_of_flashes

    if not np.any(m):
        step_when_all_flash = step_nbr
        break

    # print(f'After step {step_nbr}:')
    # print_mtx(m)
    # print('')
i = 0

print(f'Part 1. Nr of flashes: {part1_nr_of_flashes}')
print(f'Part 2. step_when_all_flash ', step_when_all_flash)

t2 = timer()
print(f'time: {(t2-t1):.4f}s')
