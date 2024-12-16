import math
import re
import copy
from collections import Counter

import sys
import os
import time
import heapq

# silly python path manipulation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.grid import Grid


def parse(filename: str) -> tuple[Grid, Grid.Pos, list[str]]:
    with open(filename) as f:
        content = f.read().strip()

    lines = content.split("\n")
    rows = len(lines)
    cols = len(lines[0])
    grid = Grid(rows, cols)

    start = None
    end = None

    for row, line in enumerate(lines):
        line = line.strip()

        for col, val in enumerate(line):
            grid.set(row, col, val)
            if val == "S":
                assert start is None
                start = Grid.Pos(row, col)
            elif val == "E":
                assert end is None
                end = Grid.Pos(row, col)

            grid.set(row, col, val)

    return grid, start, end


def dijkstra(grid: Grid, start: Grid.Pos, end: Grid.Pos) -> int:
    pq = [(0, start)]  # priority queue of tuples (accumulated cost, position)
    visited = set()

    while pq:
        acc_cost, pos = heapq.heappop(pq)
        if pos in visited:
            continue
        visited.add(pos)

        if pos == end:
            return acc_cost

        for direction in [Grid.Pos(0, 1), Grid.Pos(0, -1), Grid.Pos(1, 0), Grid.Pos(-1, 0)]:
            new_pos = pos + direction

            cell_value = grid.get_by_pos(new_pos)
            if cell_value == "#":
                continue

            if new_pos in visited:
                continue

            new_cost = acc_cost + 1
            heapq.heappush(pq, (new_cost, new_pos))

    return -1  # return -1 if no path is found


def part1(grid: Grid, start: Grid.Pos, end: Grid.Pos):
    grid.print_grid()
    cost = dijkstra(grid, start, end)
    print(cost)
    print("Part 1:", -1)


def part2(grid: Grid, start: Grid.Pos, end: Grid.Pos):
    print("Part 2:", -1)


filename = "day16/example"
# filename = "day16/input"

grid, start, end = parse(filename)
part1(grid, start, end)
# part2(grid)
