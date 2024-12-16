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

EAST = Grid.Pos(0, 1)
WEST = Grid.Pos(0, -1)
NORTH = Grid.Pos(-1, 0)
SOUTH = Grid.Pos(1, 0)


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


def dijkstra(grid: Grid, start: Grid.Pos, end: Grid.Pos) -> tuple[int, list[Grid.Pos]]:
    pq = [(0, start, EAST, [])]  # priority queue of tuples (accumulated cost, position, previous direction, path)
    visited = set()

    while pq:
        curr_cost, curr_pos, prev_d, path = heapq.heappop(pq)
        if curr_pos in visited:
            continue
        visited.add(curr_pos)

        path = path + [curr_pos]

        if curr_pos == end:
            return curr_cost, path

        for d in [EAST, WEST, NORTH, SOUTH]:
            next_pos = curr_pos + d

            cell_value = grid.get_by_pos(next_pos)
            if cell_value == "#":
                continue

            if next_pos in visited:
                continue

            step_cost = 1

            if prev_d.row != d.row and prev_d.col != d.col:
                step_cost += 1000

            heapq.heappush(pq, (curr_cost + step_cost, next_pos, d, path))

    return -1, []  # return -1 and empty path if no path is found


def dfs_all_paths(grid: Grid, start: Grid.Pos, end: Grid.Pos, lowest_cost: int) -> list[set[Grid.Pos]]:
    def dfs(curr_pos: Grid.Pos, facing: Grid.Pos, visited: set[Grid.Pos], curr_cost: int):
        if curr_cost > lowest_cost:
            return

        if curr_pos == end:
            tiles.update(visited)
            return

        for d in [EAST, WEST, NORTH, SOUTH]:
            new_pos = curr_pos + d

            if new_pos in visited:
                continue

            if grid.get_by_pos(new_pos) == "#":
                continue

            step_cost = 1

            if d != facing:
                step_cost += 1000

            visited.add(new_pos)
            dfs(new_pos, d, visited, curr_cost + step_cost)
            visited.remove(new_pos)

    tiles = set()
    dfs(start, EAST, {start}, 0)
    return tiles


def print_path(grid: Grid, path: list[Grid.Pos]):
    grid_copy = grid.copy()

    # set directions
    next_dir = EAST
    for i, pos in enumerate(path):
        if i == 0 or i == len(path) - 1:
            continue

        next_dir = path[i + 1] - path[i]

        if next_dir == EAST:
            grid_copy.set_by_pos(pos, ">")
        elif next_dir == WEST:
            grid_copy.set_by_pos(pos, "<")
        elif next_dir == NORTH:
            grid_copy.set_by_pos(pos, "^")
        elif next_dir == SOUTH:
            grid_copy.set_by_pos(pos, "v")

    # draw glorious grid with path
    for row in range(grid_copy.rows):
        line = ""
        for col in range(grid_copy.cols):
            pos = Grid.Pos(row, col)
            line += grid_copy.get_by_pos(pos)
        print(line)


def print_tiles(grid: Grid, paths: list[list[Grid.Pos]]):
    grid_copy = grid.copy()

    for path in paths:
        for pos in path:
            grid_copy.set_by_pos(pos, "O")

    # draw glorious grid with path
    for row in range(grid_copy.rows):
        line = ""
        for col in range(grid_copy.cols):
            pos = Grid.Pos(row, col)
            line += grid_copy.get_by_pos(pos)
        print(line)


def solve(grid: Grid, start: Grid.Pos, end: Grid.Pos):
    # grid.print_grid()
    lowest_cost, path = dijkstra(grid, start, end)
    print("Part 1 lowest cost:", lowest_cost)
    # print_path(grid, path)

    tiles = dfs_all_paths(grid, start, end, lowest_cost)

    ans = len(tiles)

    print("Part 2:", ans)


start_time = time.perf_counter()

# filename = "day16/example"
filename = "day16/input"

grid, start, end = parse(filename)
solve(grid, start, end)

end_time = time.perf_counter()
print(f"Total time: {end_time - start_time} seconds")
