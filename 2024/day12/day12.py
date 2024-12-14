import math
import re
import copy
from collections import Counter, defaultdict

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


def count_corners(grid: Grid, region: list[Pos]) -> int:
    assert len(region) > 0

    if len(region) == 1 or len(region) == 2:
        return 4

    rows = len(grid)
    cols = len(grid[0])

    # make a friendly grid that defaults to "." when we're out of bounds
    friendlygrid = defaultdict(str)
    for r in range(rows):
        for c in range(cols):
            friendlygrid[(r, c)] = grid[r][c]

    corners = 0
    for r, c in region:
        up = friendlygrid[(r - 1, c)]
        right = friendlygrid[(r, c + 1)]
        down = friendlygrid[(r + 1, c)]
        left = friendlygrid[(r, c - 1)]
        up_right = friendlygrid[(r - 1, c + 1)]
        down_right = friendlygrid[(r + 1, c + 1)]
        down_left = friendlygrid[(r + 1, c - 1)]
        up_left = friendlygrid[(r - 1, c - 1)]

        curr = friendlygrid[(r, c)]

        # convex corners
        if curr != up and curr != right:
            corners += 1
        if curr != up and curr != left:
            corners += 1
        if curr != down and curr != right:
            corners += 1
        if curr != down and curr != left:
            corners += 1

        # concave corners
        if curr == up and curr == right and curr != up_right:
            corners += 1
        if curr == up and curr == left and curr != up_left:
            corners += 1
        if curr == down and curr == right and curr != down_right:
            corners += 1
        if curr == down and curr == left and curr != down_left:
            corners += 1

    return corners


def solve(grid):
    cumulative_regions = set()

    total_price_p1 = 0
    total_price_p2 = 0

    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if (r, c) in cumulative_regions:
                continue
            region = flood_fill_region(grid, r, c)

            area = area_of_region(region)
            perimeter = perimeter_of_region(grid, region)
            corners = count_corners(grid, region)

            price_p1 = area * perimeter
            total_price_p1 += price_p1

            price_p2 = area * corners
            total_price_p2 += price_p2

            # print(f"A Region of {grid[r][c]} plants with price {area} * {perimeter} = {price_p1}.")

            cumulative_regions.update(region)

    assert total_price_p1 == 1424472
    print("Part 1:", total_price_p1)

    assert total_price_p2 == 870202
    print("Part 2:", total_price_p2)


# filename = "day12/example"
filename = "day12/input"

grid = parse(filename)
solve(grid)
