from dataclasses import dataclass
import time
import math
import re
import copy
from collections import Counter
import sys
import os
from collections import defaultdict

# silly python path manipulation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.grid import Grid
import utils.parse_utils as parse_utils

rows = 7
cols = 5


def parse(filename: str) -> tuple[list[Grid], list[Grid]]:
    with open(filename) as f:
        sections = f.read().strip().split("\n\n")

    locks: list[Grid] = []
    keys: list[Grid] = []

    for section in sections:
        lines = section.split("\n")
        grid = Grid(rows, cols)
        for row in range(rows):
            for col in range(cols):
                grid.set(row, col, lines[row][col])

        if lines[0] == "#####":
            locks.append(grid)
        else:
            keys.append(grid)

    return locks, keys


def to_heights(grid: Grid) -> list[int]:
    heights = [0] * cols
    for col in range(cols):
        height = 0
        for row in range(rows):
            if grid.get(row, col) == "#":
                height += 1
        heights[col] = height - 1

    return heights


def part1(locks: list[Grid], keys: list[Grid]):
    fit_cnt = 0
    for i in range(len(locks)):
        lock = locks[i]
        lock_heights = to_heights(lock)
        for j in range(len(keys)):
            key = keys[j]
            key_heights = to_heights(key)
            fits = True

            for k in range(cols):
                if key_heights[k] + lock_heights[k] > 5:
                    fits = False
                    break
            if fits:
                print(f"Lock {lock_heights} and key {key_heights}: all columns fit.")
                fit_cnt += 1
            else:
                print(f"Lock {lock_heights} and key {key_heights}: not all columns fit.")

    print("Part 1:", fit_cnt)


filename = "day25/example"
filename = "day25/input"

locks, keys = parse(filename)
part1(locks, keys)
