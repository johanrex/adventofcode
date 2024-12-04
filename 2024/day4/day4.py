import math
import re
import copy
from collections import Counter

xmas = "XMAS"
xmas_reverse = xmas[::-1]


def parse_strs(filename: str):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]
    return lines


def print_grid(grid):
    for row in grid:
        print(row)


def rotate_grid_cw(grid: list[str]) -> list[str]:
    assert len(grid) == len(grid[0])

    n = len(grid)
    rotated = []
    for i in range(n):
        new_row = ""
        for j in range(n):
            new_row += grid[n - j - 1][i]
        rotated.append(new_row)
    return rotated


def get_diagonals(grid: list[str]) -> list[str]:
    n = len(grid)
    diagonals = []
    for c in range(2 * n - 1):
        diagonal = ""
        for r in range(n):
            if 0 <= c - r < n:
                diagonal += grid[r][c - r]
        diagonals.append(diagonal)
    return diagonals


def flip_grid(grid: list[str]) -> list[str]:
    flipped = []
    for row in grid:
        flipped.append(row[::-1])
    return flipped


def part1(grid):
    cnt = 0

    for row in grid:
        matches = re.finditer(xmas, row)
        cnt += len(list(matches))
        matches = re.finditer(xmas_reverse, row)
        cnt += len(list(matches))

    grid_r = rotate_grid_cw(grid)
    for row in grid_r:
        matches = re.finditer(xmas, row)
        cnt += len(list(matches))
        matches = re.finditer(xmas_reverse, row)
        cnt += len(list(matches))

    diagonals = get_diagonals(grid)
    for diagonal in diagonals:
        matches = re.finditer(xmas, diagonal)
        cnt += len(list(matches))
        matches = re.finditer(xmas_reverse, diagonal)
        cnt += len(list(matches))

    grid_f = flip_grid(grid)
    diagonals = get_diagonals(grid_f)
    for diagonal in diagonals:
        matches = re.finditer(xmas, diagonal)
        cnt += len(list(matches))
        matches = re.finditer(xmas_reverse, diagonal)
        cnt += len(list(matches))

    assert cnt == 2642
    print("Part 1:", cnt)


def subgrid_count(grid):
    cnt = 0
    for r in range(len(grid) - 2):
        for c in range(len(grid[0]) - 2):
            subgrid = []
            for i in range(3):
                subgrid.append(grid[r + i][c : c + 3])

            # print("subgrid at r, c:", r, c)
            # print_grid(subgrid)

            if subgrid[1][1] == "A":
                if ((subgrid[0][0] == "M" and subgrid[2][2] == "S") or (subgrid[0][0] == "S" and subgrid[2][2] == "M")) and (
                    (subgrid[2][0] == "M" and subgrid[0][2] == "S") or (subgrid[2][0] == "S" and subgrid[0][2] == "M")
                ):
                    cnt += 1
                    # print("found mas x")
                    # print("cnt:", cnt)
            pass
    return cnt


def part2(grid):
    cnt = subgrid_count(grid)
    assert cnt == 1974
    print("Part 2:", cnt)


# filename = "day4/example"
filename = "day4/input"

grid = parse_strs(filename)
part1(grid)
part2(grid)
