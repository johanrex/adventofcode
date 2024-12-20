import heapq
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

EAST = Grid.Pos(0, 1)
WEST = Grid.Pos(0, -1)
NORTH = Grid.Pos(-1, 0)
SOUTH = Grid.Pos(1, 0)


def parse(filename: str) -> tuple[Grid, Grid.Pos, Grid.Pos]:
    with open(filename) as f:
        content = f.read()
        lines = [line.strip() for line in content.strip().splitlines()]

    start = None
    end = None
    grid = Grid(len(lines), len(lines[0]))
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            pos = Grid.Pos(row, col)
            grid.set_by_pos(pos, char)
            if char == "S":
                start = pos
            elif char == "E":
                end = pos
    return grid, start, end


def dijkstra(grid: Grid, start: Grid.Pos) -> dict[Grid.Pos, int]:
    # priority queue: (distance, pos)
    pq = [(0, start)]

    distances = defaultdict(lambda: sys.maxsize)
    distances[start] = 0

    visited = set()

    while pq:
        curr_dist, curr_pos = heapq.heappop(pq)

        if curr_pos in visited:
            continue

        visited.add(curr_pos)

        for step in [EAST, WEST, NORTH, SOUTH]:
            next_pos = curr_pos + step

            if not grid.is_pos_within_bounds(next_pos):
                continue

            val = grid.get_by_pos(next_pos)
            if val == "#":
                continue

            next_dist = curr_dist + 1

            # If a shorter path to the neighbor is found
            if next_dist < distances[next_pos]:
                distances[next_pos] = next_dist
                heapq.heappush(pq, (next_dist, next_pos))

    return distances


def part1(grid: Grid, start: Grid.Pos, end: Grid.Pos):
    dists = dijkstra(grid, start)

    d = dists[end]
    print(d)

    print("Part 1:", -1)


filename = "day20/example"
# filename = "day20/input"

grid, start, end = parse(filename)
part1(grid, start, end)
