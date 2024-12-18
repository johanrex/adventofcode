import heapq
import time
import math
import re
import copy
from collections import Counter
import sys
import os


# silly python path manipulation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.grid import Grid

rows = None
cols = None

EAST = Grid.Pos(0, 1)
WEST = Grid.Pos(0, -1)
NORTH = Grid.Pos(-1, 0)
SOUTH = Grid.Pos(1, 0)


def parse(filename: str) -> list[Grid.Pos]:
    positions = []
    with open(filename) as f:
        for line in f:
            tmp = list(map(int, re.findall(r"\d+", line)))
            positions.append(Grid.Pos(tmp[1], tmp[0]))
    return positions


def make_grid(positions: list[Grid.Pos]) -> Grid:
    global rows, cols
    if rows is None:
        rows = max([pos.row for pos in positions]) + 1
        cols = max([pos.col for pos in positions]) + 1
    grid = Grid(rows, cols, ".")

    # print(grid.rows, grid.cols)

    for pos in positions:
        grid.set_by_pos(pos, "#")
    return grid


def dijkstra(grid: Grid, start: Grid.Pos) -> dict[Grid.Pos, int]:
    # (distance, pos)
    pq = [(0, start)]

    # init distances
    distances = dict()
    for row in range(grid.rows):
        for col in range(grid.cols):
            pos = Grid.Pos(row, col)
            val = grid.get_by_pos(pos)
            if val != "#":
                distances[pos] = float("inf")

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


def part1(filename: str):
    positions = parse(filename)

    if "example" in filename:
        positions = positions[:12]
    else:
        positions = positions[:1024]

    grid = make_grid(positions)
    start = Grid.Pos(0, 0)
    end = Grid.Pos(grid.rows - 1, grid.cols - 1)

    assert grid.get_by_pos(start) == "."
    assert grid.get_by_pos(end) == "."

    distances = dijkstra(grid, start)

    shortest_dist = distances[end]

    print("Part 1:", shortest_dist)


def part2(filename: str):
    positions = parse(filename)

    if "example" in filename:
        lower_bound = 1
    else:
        lower_bound = 1024

    found = False
    for i in range(lower_bound, len(positions)):
        print(i)
        tmp_positions = positions[:i]

        grid = make_grid(tmp_positions)
        start = Grid.Pos(0, 0)
        end = Grid.Pos(grid.rows - 1, grid.cols - 1)

        assert grid.get_by_pos(start) == "."
        assert grid.get_by_pos(end) == "."

        distances = dijkstra(grid, start)

        shortest_dist = distances[end]

        # grid.print_grid()
        # print("")

        if shortest_dist == float("inf"):
            found = True
            break

    if found:
        pos = positions[i - 1]
        msg = f"{pos.col},{pos.row}"
        print("Part 2:", msg)
    else:
        print("Part 2: Not found")


# filename = "day18/example"
filename = "day18/input"


part1(filename)
part2(filename)
