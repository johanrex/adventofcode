from typing import List
import copy

def parse_input(filename)-> List[List[str]]:
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(list(line.strip()))

    return lines


def print_grid(grid):
    for row in grid:
        print(''.join(row))

    print('')

def step(grid):

    row_count = len(grid)
    col_count = len(grid[0])

    something_moved = False

    output_stage1 = copy.deepcopy(grid)

    #move right
    for row in range(row_count):
        for col in range(col_count):
            if grid[row][col] == '.':

                prev_col = col_count - 1 if col == 0 else col - 1
                prev_col_val = grid[row][prev_col]
                if prev_col_val == '>': 
                    output_stage1[row][prev_col] = '.'
                    output_stage1[row][col] = '>'

                    something_moved = True

    output_stage2 = copy.deepcopy(output_stage1)

    #move down
    for row in range(row_count):
        for col in range(col_count):
            if output_stage1[row][col] == '.':
                prev_row = row_count - 1 if row == 0 else row - 1
                prev_row_val = output_stage1[prev_row][col]

                if prev_row_val == 'v':
                    output_stage2[prev_row][col] = '.'
                    output_stage2[row][col] = 'v'

                    something_moved = True

    return output_stage2, something_moved


filename = '2021/25_input.txt'
#filename = '2021/25_input_example.txt'

grid = parse_input(filename)

# print('Initial state:')
# print_grid(grid)

for i in range(1000):

    grid, something_moved = step(grid)

    # print(f'After {i+1} steps:')
    # print_grid(grid)

    if not something_moved:
        print('Part 1. First step something didn''t move:', i+1)
        break

print('Done.')

i=0

