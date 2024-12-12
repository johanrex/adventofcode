import math
import re
import copy
from collections import Counter

Grid = list[list[str]]
Pos = tuple[int, int]

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def parse(filename: str) -> Grid:
    grid = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            line = [c for c in line]
            grid.append(line)
    return grid


def get_neighbors(grid: Grid, r: int, c: int) -> list[Pos]:
    rows = len(grid)
    cols = len(grid[0])

    assert r >= 0 and r < rows and c >= 0 and c < cols

    neighbors = []
    for dir in DIRS:
        new_r, new_c = r + dir[0], c + dir[1]
        if new_r >= 0 and new_r < rows and new_c >= 0 and new_c < cols:
            neighbors.append((new_r, new_c))

    return neighbors


def flood_fill_region(grid: Grid, r: int, c: int) -> set[Pos]:
    def flood_fill_recursive(grid, r, c, visited: set[Pos], filled: set[Pos], val: str):
        if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]):
            return

        if (r, c) in visited:
            return

        visited.add((r, c))

        if grid[r][c] == val:
            filled.add((r, c))
        else:
            return

        neighbors = get_neighbors(grid, r, c)
        for neighbor in neighbors:
            if neighbor not in visited:
                flood_fill_recursive(grid, neighbor[0], neighbor[1], visited, filled, val)

    val = grid[r][c]
    region = set()
    visited = set()
    flood_fill_recursive(grid, r, c, visited, region, val)
    return region


def area_of_region(region: set[Pos]) -> int:
    return len(region)


def perimeter_of_region(grid: Grid, region: set[Pos]) -> int:
    r, c = next(iter(region))
    region_val = grid[r][c]

    perimeter = 0

    for r, c in region:
        neighbors = get_neighbors(grid, r, c)
        perimeter += 4 - len(neighbors)
        for n_r, n_c in neighbors:
            if grid[n_r][n_c] != region_val:
                perimeter += 1

    return perimeter


def part1(grid):
    cumulative_regions = set()

    total_price = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if (r, c) in cumulative_regions:
                continue
            region = flood_fill_region(grid, r, c)

            area = area_of_region(region)
            assert area > 0

            perimeter = perimeter_of_region(grid, region)
            price = area * perimeter
            print(f"A Region of {grid[r][c]} plants with price {area} * {perimeter} = {price}:")
            total_price += price
            cumulative_regions.update(region)

    print("Part 1:", total_price)


def part2(grid):
    print("Part 2:", -1)


# filename = "day12/example"
filename = "day12/input"

grid = parse(filename)
part1(grid)
# part2(grid)
