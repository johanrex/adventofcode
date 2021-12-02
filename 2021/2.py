
def get_input():
    with(open("2021/2_input.txt", "r")) as f:
        lines = f.readlines()

    return lines

lines = get_input()

import re

p = re.compile(r'([a-z]*) (\d*)')

sum_h = 0
sum_d = 0

for line in lines:
    m = p.match(line)

    direction = m.group(1)
    distance = int(m.group(2))

    if direction == 'up':
        sum_h -= distance
    if direction == 'down':
        sum_h += distance    
    if direction == 'forward':
        sum_d += distance    

    #print(f'{direction} {distance}')

print(f'horizontal: {sum_h}, depth: {sum_d}')
print(f'multiplied: {sum_h * sum_d}')

