import math
import re
import copy
from collections import Counter

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def parse(filename: str):
    grid = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            line = list(map(int, [c for c in line]))

            grid.append(line)
    return grid


def print_grid(grid):
    for row in grid:
        print("".join(map(str, row)))


def find_neighbors(grid, r, c):
    neighbors = []
    for dir in DIRS:
        new_r = r + dir[0]
        new_c = c + dir[1]
        if new_r >= 0 and new_r < len(grid) and new_c >= 0 and new_c < len(grid[0]):
            neighbors.append((new_r, new_c))

    return neighbors


def find_all(grid, value):
    all = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == value:
                all.append((r, c))
    return all


def dfs_with_path(grid, start, target):
    def dfs_recursive(pos, visited, path):
        r, c = pos

        # Base cases
        if not (0 <= r < len(grid) and 0 <= c < len(grid[0])):
            return None
        if pos in visited:
            return None
        if grid[r][c] == target:
            return path + [pos]

        # Mark as visited and add to current path
        visited.add(pos)

        # Try all neighbors
        for neighbor in find_neighbors(grid, r, c):
            result = dfs_recursive(neighbor, visited, path + [pos])
            if result:
                return result

        return None

    return dfs_recursive(start, set(), [])


def part1(grid):
    print_grid(grid)
    starts = find_all(grid, 0)

    shortest_path = None
    for start in starts:
        path = dfs_with_path(grid, start, 9)
        if path and (not shortest_path or len(path) < len(shortest_path)):
            shortest_path = path

    if shortest_path:
        print("Found path:", shortest_path)
        print("Part 1:", len(shortest_path) - 1)
    else:
        print("Part 1: No path found")


def part2(grid):
    print("Part 2:", -1)


filename = "day10/example"
# filename = "day10/input"

grid = parse(filename)
part1(grid)
# part2(grid)
