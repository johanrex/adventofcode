from dataclasses import dataclass
import time
import math
import re
import copy
from collections import Counter, deque
import sys
import os
from collections import defaultdict
import itertools
import matplotlib.pyplot as plt

# silly python path manipulation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.grid import Grid
import utils.parse_utils as parse_utils


def parse(filename: str) -> list[tuple[int, int]]:
    coords = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            a, b = line.split(",")
            coords.append((int(a), int(b)))

    return coords


def part1(coords):
    max_area = -1
    for i in range(len(coords)):
        row1, col1 = coords[i]
        for j in range(i + 1, len(coords)):
            row2, col2 = coords[j]

            area = (abs(col1 - col2) + 1) * (abs(row1 - row2) + 1)
            max_area = max(max_area, area)

    print("Part 1:", max_area)


def show_polygon(coords):
    xs = [x for x, y in coords]
    ys = [y for x, y in coords]
    # close the polygon for plotting
    xs_closed = xs + [xs[0]]
    ys_closed = ys + [ys[0]]

    plt.figure(figsize=(6, 6))
    plt.plot(xs_closed, ys_closed, "-o", markersize=3)
    plt.axis("equal")
    plt.grid(True, linestyle=":", alpha=0.5)
    plt.title("Polygon")
    plt.show()


def fill_edges(grid: Grid, polygon: list[tuple[int, int]]):
    # fill outside edges

    # make a closed loop
    coords_to_walk = deque(polygon[:] + [polygon[0]])

    prev = coords_to_walk.popleft()
    while len(coords_to_walk) > 1:
        curr = coords_to_walk.popleft()

        # print(f"{prev} -> {curr}")

        # find out if we are moving horizontally or vertically
        if prev[0] != curr[0] and prev[1] == curr[1]:  # vertical movement
            row_start = min(prev[0], curr[0])
            row_end = max(prev[0], curr[0])
            col = prev[1]

            for r in range(row_start, row_end + 1):
                grid.set(r, col, "#")

        elif prev[1] != curr[1] and prev[0] == curr[0]:  # horizontal movement
            col_start = min(prev[1], curr[1])
            col_end = max(prev[1], curr[1])
            row = prev[0]

            for c in range(col_start, col_end + 1):
                grid.set(row, c, "#")

        else:
            raise ValueError("Only horizontal or vertical edges are supported")

        prev = curr
        pass

    pass


def is_rectangle_inside_polygon(
    grid: Grid, row1: int, col1: int, row2: int, col2: int
) -> bool:
    # ray cast from all four corners

    min_row = min(row1, row2)
    max_row = max(row1, row2)
    min_col = min(col1, col2)
    max_col = max(col1, col2)

    topleft = (min_row, min_col)
    topright = (min_row, max_col)
    bottomleft = (max_row, min_col)
    bottomright = (max_row, max_col)


def part2(coords):
    # create polygon
    # flood fill inside
    # for each pair of coords, check that all corners are inside and the diagonal doesn't cross outside

    show_polygon(coords)

    grid = Grid(sys.maxsize, sys.maxsize, default_value=".")

    # coords is assumed to be a closed polygon
    fill_edges(grid, coords)

    # pray that this works to find a starting point inside the polygon
    min_row = min(r for r, c in coords)
    top_cols = [c for r, c in coords if r == min_row]
    assert len(top_cols) == 2
    middle_col = sum(top_cols) // 2
    assert grid.get(min_row + 1, middle_col) == "."

    # TODO ray casting instead of flood fill
    # Two standard algorithms for point-in-polygon:

    #     Ray casting (even–odd rule)

    #     Idea: Cast a ray from the point to infinity (typically horizontally). Count how many times it intersects polygon edges. Odd = inside; even = outside.
    #     Complexity: O(n) for n edges.
    #     Pros: Simple to implement.
    #     Edge cases: Handle points exactly on edges/vertices; avoid counting intersections at vertex twice; treat horizontal edges carefully.

    # flood_fill(grid, min_row + 1, middle_col)

    max_area = -1
    for i in range(len(coords)):
        row1, col1 = coords[i]
        for j in range(i + 1, len(coords)):
            row2, col2 = coords[j]

            if is_rectangle_inside_polygon(grid, row1, col1, row2, col2):
                area = (abs(col1 - col2) + 1) * (abs(row1 - row2) + 1)
                max_area = max(max_area, area)


filename = "day09/example"
filename = "day09/input"

coords = parse(filename)
# part1(coords)
part2(coords)
