import math
import re
import copy
from collections import Counter
import sys


DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

Pos = tuple[int, int]
Grid = list[list[int]]


def parse(filename: str):
    grid = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            lst = [c if c.isdigit() else "-9" for c in line]
            line = list(map(int, [c for c in lst]))

            grid.append(line)
    return grid


def print_grid(grid: Grid):
    for row in grid:
        row = ["." if c == -9 else str(c) for c in row]

        print("".join(map(str, row)))


def print_grid_and_color_path(grid: Grid, path: list[Pos]):
    for r, row in enumerate(grid):
        row = ["." if c == -9 else str(c) for c in row]

        for c, val in enumerate(row):
            if (r, c) in path:
                color_start = "\033[92m"
                color_end = "\033[0m"
                print(color_start + val + color_end, end="")
            else:
                print(val, end="")

        print()  # newline


def find_neighbors(grid: Grid, r: int, c: int) -> list[Pos]:
    neighbors = []
    for dir in DIRS:
        new_r = r + dir[0]
        new_c = c + dir[1]
        if new_r >= 0 and new_r < len(grid) and new_c >= 0 and new_c < len(grid[0]):
            neighbors.append((new_r, new_c))

    return neighbors


def find_all_pos(grid: Grid, value: int) -> list[Pos]:
    all = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == value:
                all.append((r, c))
    return all


def all_paths_recursive(grid: Grid, start_pos: Pos, end_value: int):
    paths = []
    visited = set()
    visited.add(start_pos)

    def dfs(pos: Pos, path: list[Pos]):
        if grid[pos[0]][pos[1]] == end_value:
            paths.append(path)
            return

        curr_val = grid[pos[0]][pos[1]]

        neighbors = find_neighbors(grid, pos[0], pos[1])
        for neighbor in neighbors:
            neighbor_val = grid[neighbor[0]][neighbor[1]]
            if neighbor_val == curr_val + 1 and neighbor not in visited:
                visited.add(neighbor)
                dfs(neighbor, path + [neighbor])
                visited.remove(neighbor)

    dfs(start_pos, [start_pos])
    return paths


def part1(grid: Grid):
    print_grid(grid)
    all_zero_pos = find_all_pos(grid, 0)

    sum_of_scores = 0
    for zero_pos in all_zero_pos:
        paths = all_paths_recursive(grid, zero_pos, 9)

        # nr of unique 9s reached from trail head
        trailhead_score = len(set([path[-1] for path in paths]))

        sum_of_scores += trailhead_score

        # for i, path in enumerate(paths):
        #     print("path:", path)
        #     print(f"({i+1}/{len(paths)})")
        #     print_grid_and_color_path(grid, path)
        #     pass

    # print(all_paths)
    print("Part 1:", sum_of_scores)


def part2(grid: Grid):
    print("Part 2:", -1)


# filename = "day10/example"
filename = "day10/input"

grid = parse(filename)
part1(grid)
# part2(grid)
