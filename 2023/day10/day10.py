from dataclasses import dataclass
import math
import re
from collections import deque


def parse(filename):
    grid = []
    with open(filename) as f:
        for line in f:
            chars = [c for c in line.strip()]
            grid.append(chars)
    return grid


def find_s(grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == "S":
                return row, col


def get_neighbors(grid, vertex):
    row, col = vertex
    neighbors = []

    if grid[row][col] == "S":
        west = grid[row][col - 1] if col > 0 else None
        if west is not None and west in "SFL-":
            neighbors.append((row, col - 1))

        east = grid[row][col + 1] if col < len(grid[row]) - 1 else None
        if east is not None and east in "SJ7-":
            neighbors.append((row, col + 1))

        north = grid[row - 1][col] if row > 0 else None
        if north is not None and north in "SF7|":
            neighbors.append((row - 1, col))

        south = grid[row + 1][col] if row < len(grid) - 1 else None
        if south is not None and south in "SJL|":
            neighbors.append((row + 1, col))

    elif grid[row][col] == "|":
        north = grid[row - 1][col] if row > 0 else None
        if north is not None and north in "SF7|":
            neighbors.append((row - 1, col))

        south = grid[row + 1][col] if row < len(grid) - 1 else None
        if south is not None and south in "SJL|":
            neighbors.append((row + 1, col))

    elif grid[row][col] == "-":
        west = grid[row][col - 1] if col > 0 else None
        if west is not None and west in "SFL-":
            neighbors.append((row, col - 1))

        east = grid[row][col + 1] if col < len(grid[row]) - 1 else None
        if east is not None and east in "SJ7-":
            neighbors.append((row, col + 1))

    elif grid[row][col] == "L":
        north = grid[row - 1][col] if row > 0 else None
        if north is not None and north in "SF7|":
            neighbors.append((row - 1, col))

        east = grid[row][col + 1] if col < len(grid[row]) - 1 else None
        if east is not None and east in "SJ7-":
            neighbors.append((row, col + 1))

    elif grid[row][col] == "J":
        north = grid[row - 1][col] if row > 0 else None
        if north is not None and north in "SF7|":
            neighbors.append((row - 1, col))

        west = grid[row][col - 1] if col > 0 else None
        if west is not None and west in "SFL-":
            neighbors.append((row, col - 1))

    elif grid[row][col] == "7":
        south = grid[row + 1][col] if row < len(grid) - 1 else None
        if south is not None and south in "SJL|":
            neighbors.append((row + 1, col))

        west = grid[row][col - 1] if col > 0 else None
        if west is not None and west in "SFL-":
            neighbors.append((row, col - 1))

    elif grid[row][col] == "F":
        south = grid[row + 1][col] if row < len(grid) - 1 else None
        if south is not None and south in "SJL|":
            neighbors.append((row + 1, col))

        east = grid[row][col + 1] if col < len(grid[row]) - 1 else None
        if east is not None and east in "SJ7-":
            neighbors.append((row, col + 1))

    return neighbors


def print_path(grid, path):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if (row, col) in path:
                print(grid[row][col], end="")
            else:
                print(".", end="")
        print()


def find_cycle(start_vertex, grid):
    visited = set()
    path = []

    def visit(vertex, parent):
        visited.add(vertex)
        path.append(vertex)

        neighbors = get_neighbors(grid, vertex)

        for neighbor in neighbors:
            if neighbor not in visited:
                if visit(neighbor, vertex):
                    return True
            elif neighbor != parent:  # Ignore the edge to the parent node
                # Cycle detected. Keep only the nodes in the cycle.
                while path[0] != neighbor:
                    path.pop(0)
                return True

        path.pop()
        return False

    if not visit(start_vertex, None):
        raise ValueError("No cycle found")

    return path


def part1(grid):
    row, col = find_s(grid)
    # row, col = 1, 1

    path = find_cycle((row, col), grid)

    print(path)

    print_path(grid, path)
    farthest_cell = math.ceil(len(path) / 2)

    print("Part 1:", farthest_cell)


def part2(lines):
    print("Part 2:", lines)


# filename = "day10/example"
filename = "day10/input"

grid = parse(filename)
part1(grid)
# part2(grid)
