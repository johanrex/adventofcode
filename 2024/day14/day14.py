from dataclasses import dataclass
import math
import re
import copy
from collections import Counter


@dataclass
class Robot:
    r: int
    c: int
    v_r: int
    v_c: int


def parse(filename: str):
    robots = []
    with open(filename) as f:
        for line in f:
            nrs = list(map(int, re.findall(r"-?\d+", line)))
            robot = Robot(nrs[1], nrs[0], nrs[3], nrs[2])
            robots.append(robot)
    return robots


def print_grid(robots: list[Robot], rows: int, cols: int):
    grid = [["." for _ in range(cols)] for _ in range(rows)]

    robot_positions = [(robot.r, robot.c) for robot in robots]
    counter = Counter(robot_positions)

    for r in range(rows):
        for c in range(cols):
            if (r, c) in counter:
                grid[r][c] = str(counter[(r, c)])

    for row in grid:
        print("".join(row))
    print("")


def move(robots: list[Robot], rows: int, cols: int):
    for robot in robots:
        robot.r += robot.v_r
        robot.c += robot.v_c

        # Wrap around if out of bounds
        if robot.r < 0:
            robot.r = rows + robot.r
        if robot.r >= rows:
            robot.r = robot.r - rows
        if robot.c < 0:
            robot.c = cols + robot.c
        if robot.c >= cols:
            robot.c = robot.c - cols


def calc_safety_factor(robots: list[Robot], rows: int, cols: int):
    q1 = 0
    q2 = 0
    q3 = 0
    q4 = 0
    for robot in robots:
        if robot.r == rows // 2 or robot.c == cols // 2:
            continue

        if robot.r < rows // 2 and robot.c < cols // 2:
            q1 += 1
        elif robot.r < rows // 2 and robot.c > cols // 2:
            q2 += 1
        elif robot.r > rows // 2 and robot.c < cols // 2:
            q3 += 1
        else:
            q4 += 1

    return q1 * q2 * q3 * q4


def part1(robots):
    # example
    # robots = [robots[10]]

    print("Initial state:")
    print_grid(robots, rows, cols)

    second = 0
    for second in range(100):
        move(robots, rows, cols)
        # print(f"After {second+1} seconds:")
        # print_grid(robots, rows, cols)
        pass

    print(f"After {second+1} seconds:")
    print_grid(robots, rows, cols)

    safety_factor = calc_safety_factor(robots, rows, cols)

    print("Part 1:", safety_factor)


def part2(robots):
    print("Part 2:", -1)


# filename = "day14/example"
filename = "day14/input"

if "example" in filename:
    cols = 11
    rows = 7
else:
    cols = 101
    rows = 103

robots = parse(filename)
part1(robots)
# part2(robots)
