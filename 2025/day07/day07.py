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


def parse(filename: str) -> Grid:
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]

    grid = Grid(len(lines), len(lines[0]), default_value=".")
    for row_idx, line in enumerate(lines):
        for col_idx, ch in enumerate(line):
            if ch != ".":
                grid.set(row_idx, col_idx, ch)

    return grid


splitters_reached = set()


def beam_from_point(grid: Grid, start_row: int, start_col: int):
    if start_row >= grid.rows or start_col < 0 or start_col >= grid.cols:
        return

    row_idx = start_row
    col_idx = start_col

    curr_val = grid.get(row_idx, col_idx)

    if curr_val == ".":
        grid.set(row_idx, col_idx, "|")
        beam_from_point(grid, row_idx + 1, col_idx)
    elif curr_val == "^":
        splitters_reached.add((row_idx, col_idx))
        beam_from_point(grid, row_idx, col_idx - 1)
        beam_from_point(grid, row_idx, col_idx + 1)

    return


def part1(grid: Grid):
    s_col = -1
    for col_idx in range(grid.cols):
        val = grid.get(0, col_idx)
        if val == "S":
            s_col = col_idx
            break

    assert s_col != -1

    beam_from_point(grid, 1, s_col)

    ans = len(splitters_reached)

    print("Part 1:", ans)


def part2(grid: Grid):
    print("Part 2:", -1)


filename = "day07/example"
filename = "day07/input"

grid = parse(filename)
part1(grid)
# part2(grid)
