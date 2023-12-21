from dataclasses import dataclass
import math
import re
import heapq
import copy
from collections import deque
import sys

Grid = list[list[int]]


def parse(filename) -> Grid:
    grid: Grid = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            grid.append([int(c) for c in line])

    return grid


def iterative_dfs(grid, start, goal):
    stack = [start]
    visited = set()

    while stack:
        x, y = stack.pop()
        if (x, y) == goal:
            print("Goal reached")
            return
        if (x, y) in visited:
            continue
        visited.add((x, y))

        for dx, dy in [
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0),
        ]:  # 4 directions: right, down, left, up
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):  # Check boundaries
                stack.append((nx, ny))

    print("Goal not reachable")


def part1(grid: Grid):
    start = (0, 0)
    goal = (len(grid) - 1, len(grid[0]) - 1)

    pass

    # 656 too high
    # print("Part 1:", cost[goal])


def part2(grid: Grid):
    print("Part 2:", -1)


filename = "day17/example"
# filename = "day17/input"

grid = parse(filename)
part1(grid)
part2(grid)
