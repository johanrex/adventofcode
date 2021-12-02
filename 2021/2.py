import re
p = re.compile(r'([a-z]*) (\d*)')

def get_input():
    with(open("2021/2_input.txt", "r")) as f:
        lines = f.readlines()

    return lines

def parse_line(line):
    m = p.match(line)

    direction = m.group(1)
    distance = int(m.group(2))

    return direction, distance

def part_1():
    lines = get_input()

    sum_depth = 0
    sum_distance = 0

    for line in lines:

        direction, distance = parse_line(line)

        m = p.match(line)

        if direction == 'up':
            sum_depth -= distance
        if direction == 'down':
            sum_depth += distance
        if direction == 'forward':
            sum_distance += distance    

    print('--------------')
    print('Part 1')
    print('--------------')
    print(f'depth: {sum_depth}, horizontal: {sum_distance}')
    print(f'multiplied: {sum_depth * sum_distance}')

def part_2():

    lines = get_input()

    sum_depth = 0
    sum_distance = 0
    sum_aim = 0

    for line in lines:

        direction, distance = parse_line(line)

        if direction == 'up':
            sum_aim -= distance
        if direction == 'down':
            sum_aim += distance
        if direction == 'forward':
            sum_distance += distance  
            sum_depth += (distance * sum_aim)

        # print(f'{direction} {distance} -> depth:{sum_depth}, distance: {sum_distance}, aim:{sum_aim}')

    print('--------------')
    print('Part 2')
    print('--------------')
    print(f'depth: {sum_depth}, horizontal: {sum_distance}')
    print(f'multiplied: {sum_depth * sum_distance}')

part_1()
part_2()
