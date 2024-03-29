from dataclasses import dataclass
import math
import re
import matplotlib.pyplot as plt
import time


@dataclass
class Instruction:
    direction: str
    distance: int


def parse2(filename):
    plan: list[Instruction] = []

    lookup = {
        0: "R",
        1: "D",
        2: "L",
        3: "U",
    }

    with open(filename) as f:
        for line in f:
            line = line.strip()
            m = re.match(r"(\w) (\d+) \(#(\w+)\)", line)

            x = m.group(3)
            direction = lookup[int(x[-1])]
            x = x[:-1]
            distance = int(x, 16)

            plan.append(Instruction(direction, distance))

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


def create_polygon(plan: list[Instruction]) -> list[tuple[int, int]]:
    min_row, min_col, _, _ = get_bounds(plan)

    corners: list[tuple[int, int]] = []

    cur_row = min_row
    cur_col = min_col

    corners.append((cur_row, cur_col))

    for inst in plan:
        if inst.direction == "R":
            cur_col += inst.distance
        elif inst.direction == "L":
            cur_col -= inst.distance
        elif inst.direction == "U":
            cur_row -= inst.distance
        elif inst.direction == "D":
            cur_row += inst.distance

        corners.append((cur_row, cur_col))

    assert corners[0] == corners[-1]
    corners.pop()

    return corners


def polygon_area(corners: list[tuple[int, int]]) -> int:
    n = len(corners)  # Number of vertices
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    area = abs(area) / 2.0
    return int(area)


def polygon_circumference(corners):
    n = len(corners)
    circumference = 0

    for i in range(1, n):
        prev_row, prev_col = corners[i - 1]
        row, col = corners[i]

        circumference += abs(row - prev_row) + abs(col - prev_col)

    prev_row, prev_col = corners[n - 1]
    row, col = corners[0]

    circumference += abs(row - prev_row) + abs(col - prev_col)

    return circumference


def plot(corners):
    # Unpack the corners into x and y coordinates
    xs, ys = zip(*corners)

    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)

    plt.figure()
    plt.plot(xs, ys, "b")  # 'b' specifies that the color of the polygon should be blue
    plt.fill(xs, ys, "b", alpha=0.3)  # Fill the polygon with a semi-transparent blue
    plt.xlim(min_x, max_x)
    plt.ylim(min_y, max_y)
    plt.show()


def part2(plan):
    start_time = time.time()

    corners = create_polygon(plan)
    # plot(corners)

    area = polygon_area(corners)
    circumference = polygon_circumference(corners)

    n = int(area + (circumference // 2) + 1)

    print("Time:", time.time() - start_time)

    assert n == 71262565063800
    print("Part 2:", n)


filename = "day18/example"
filename = "day18/input"

plan = parse2(filename)
part2(plan)
