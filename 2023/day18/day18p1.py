from dataclasses import dataclass
import math
import re
import copy


@dataclass
class Instruction:
    direction: str
    distance: int
    color: str


def parse(filename):
    plan: list[Instruction] = []
    with open(filename) as f:
        for line in f:
            line = line.strip()

            # R 6 (#70c710)

            m = re.match(r"(\w) (\d+) \((#\w+)\)", line)

            direction = m.group(1)
            distance = int(m.group(2))
            color = m.group(3)

            plan.append(Instruction(direction, distance, color))

        return plan


def get_bounds(plan):
    min_row = 0
    min_col = 0
    max_row = 0
    max_col = 0
    cur_row = 0
    cur_col = 0

    for instruction in plan:
        if instruction.direction == "R":
            cur_col += instruction.distance
            max_col = max(cur_col, max_col)
        elif instruction.direction == "L":
            cur_col -= instruction.distance
            min_col = min(cur_col, min_col)
        elif instruction.direction == "U":
            cur_row -= instruction.distance
            min_row = min(cur_row, min_row)
        elif instruction.direction == "D":
            cur_row += instruction.distance
            max_row = max(cur_row, max_row)

    # check that we end up where we started
    assert cur_row == 0 and cur_col == 0

    return min_row, min_col, max_row, max_col


def create_grid(n_rows, n_cols):
    grid = [["." for _ in range(n_cols + 1)] for _ in range(n_rows + 1)]
    return grid


def dig(grid, instructions, start_row, start_col):
    cur_row = abs(start_row)
    cur_col = abs(start_col)

    for instruction in instructions:
        if instruction.direction == "R":
            for i in range(instruction.distance):
                cur_col += 1
                grid[cur_row][cur_col] = "#"
        elif instruction.direction == "L":
            for i in range(instruction.distance):
                cur_col -= 1
                grid[cur_row][cur_col] = "#"
        elif instruction.direction == "U":
            for i in range(instruction.distance):
                cur_row -= 1
                grid[cur_row][cur_col] = "#"
        elif instruction.direction == "D":
            for i in range(instruction.distance):
                cur_row += 1
                grid[cur_row][cur_col] = "#"

    return grid


def print_grid(grid):
    for row in grid:
        print("".join(row))


def flood_fill(grid, row, col):
    if grid[row][col] == "#":
        return

    stack = [(row, col)]

    while stack:
        r, c = stack.pop()
        if grid[r][c] == "#":
            continue

        grid[r][c] = "#"

        if r > 0:
            stack.append((r - 1, c))
        if r < len(grid) - 1:
            stack.append((r + 1, c))
        if c > 0:
            stack.append((r, c - 1))
        if c < len(grid[0]) - 1:
            stack.append((r, c + 1))


def count(grid):
    count = 0
    for row in grid:
        for col in row:
            if col == "#":
                count += 1
    return count


def find_point_inside_grid(grid):
    middle_row = len(grid) // 2

    cur_col = 0
    found_one = False
    inside = False
    while not inside:
        if not found_one and grid[middle_row][cur_col] == "#":
            found_one = True

        if found_one and grid[middle_row][cur_col + 1] == ".":
            inside = True
        cur_col += 1

    assert grid[middle_row][cur_col] != "#"

    return middle_row, cur_col


def part1(plan):
    min_row, min_col, max_row, max_col = get_bounds(plan)

    grid = create_grid(max_row - min_row, max_col - min_col)
    dig(grid, plan, start_row=min_row, start_col=min_col)
    print_grid(grid)

    row, col = find_point_inside_grid(grid)
    flood_fill(grid, row, col)

    print("Filled:")
    print_grid(grid)

    n = count(grid)
    print("Part 1:", n)


def part2(plan):
    print("Part 2:", -1)


filename = "day18/example"
filename = "day18/input"

plan = parse(filename)
part1(plan)
# part2(plan)
