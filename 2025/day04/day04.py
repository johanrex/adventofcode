from dataclasses import dataclass
import time
import math
import re
import copy
from collections import Counter
import sys
import os
from collections import defaultdict
import itertools

# silly python path manipulation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.grid import Grid
import utils.parse_utils as parse_utils


def parse(filename) -> Grid:
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]

    rows = len(lines)
    cols = len(lines[0])

    grid = Grid(rows, cols)

    for r in range(rows):
        for c in range(cols):
            grid.set(r, c, lines[r][c])

    return grid


def find_removable(grid: Grid) -> list[tuple[int, int]]:
    removable = []
    for r in range(grid.rows):
        for c in range(grid.cols):
            curr_val = grid.get(r, c)
            if curr_val == "@":
                # get neighbors in all 8 directions
                neighbor_vals = [
                    grid.get(r - 1, c - 1, default_value="."),
                    grid.get(r - 1, c, default_value="."),
                    grid.get(r - 1, c + 1, default_value="."),
                    grid.get(r, c - 1, default_value="."),
                    grid.get(r, c + 1, default_value="."),
                    grid.get(r + 1, c - 1, default_value="."),
                    grid.get(r + 1, c, default_value="."),
                    grid.get(r + 1, c + 1, default_value="."),
                ]

                cnt = neighbor_vals.count("@")
                if cnt < 4:
                    removable.append((r, c))

    return removable


def remove(grid: Grid, positions: list[tuple[int, int]]):
    for pos in positions:
        r, c = pos
        grid.set(r, c, ".")


def part1(grid: Grid):
    removable = find_removable(grid)

    print("Part 1:", len(removable))


def part2(grid: Grid):
    total_removed = 0

    while True:
        removable = find_removable(grid)
        if len(removable) == 0:
            break

        remove(grid, removable)
        total_removed += len(removable)

    print("Part 2:", total_removed)


filename = "day04/example"
filename = "day04/input"

grid = parse(filename)

part1(grid)
part2(grid)
