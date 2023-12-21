from dataclasses import dataclass
import math
import re
import copy

Grid = list[list[str]]

DIRECTIONS = ["N", "E", "S", "W"]

DIRECTION = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1),
}


def parse(filename: str) -> Grid:
    grid: Grid = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            grid.append([c for c in line])

    return grid


def get_neighbors(grid: Grid, pos: tuple[int, int]) -> list[tuple[int, int]]:
    neighbors = []
    x, y = pos
    for direction in DIRECTIONS:
        dx, dy = DIRECTION[direction]
        new_x = x + dx
        new_y = x + dy

        if (
            0 <= new_x < len(grid)
            and 0 <= new_y < len(grid[0])
            and grid[new_x][new_y] == "."
        ):
            neighbors.append((new_x, new_y))
    return neighbors


def bfs(grid: Grid, start: tuple[int, int], steps: int) -> list[tuple[int, int]]:
    visited = {}
    queue = [start]
    visited[start] = 0
    while queue:
        current = queue.pop(0)
        if visited[current] < steps:
            for neighbor in get_neighbors(grid, current):
                # if neighbor not in visited:
                visited[neighbor] = visited[current] + 1
                queue.append(neighbor)

            # dbg
            mark = [k for k, v in visited.items() if v == visited[current] + 1]
            print_grid(grid, mark)

    targets = [k for k, v in visited.items() if v == steps]
    return targets


def print_grid(grid: Grid, mark: list[tuple[int, int]]):
    g = copy.deepcopy(grid)

    for x, y in mark:
        g[x][y] = "O"

    for row in g:
        print("".join(row))

    print("")


def find_and_remove_s(grid: Grid) -> tuple[int, int]:
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if col == "S":
                grid[i][j] = "."
                return (i, j)
    assert False, "No S found"


def part1(grid):
    s = find_and_remove_s(grid)
    targets = bfs(grid, s, 6)
    print("Part 1:", len(targets))


filename = "day21/example"
# filename = "day21/input"

grid = parse(filename)
part1(grid)
