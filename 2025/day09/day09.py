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
import numpy as np
from shapely.geometry import Polygon

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
    # add coordinate labels for each point
    # for x, y in coords:
    #     plt.text(x, y, f"({x}, {y})", fontsize=6, ha="left", va="bottom")
    plt.axis("equal")
    plt.grid(True, linestyle=":", alpha=0.5)
    plt.title("Polygon")
    plt.show()


def show_grid(grid: Grid, min_row: int, max_row: int, min_col: int, max_col: int):
    """Render a rectangular slice of the Grid as an image.

    Cells with '#' are shown as black; '.' as white; anything else as gray.
    """
    height = max_row - min_row + 1
    width = max_col - min_col + 1

    # build a numeric array for imshow
    data = [[0] * width for _ in range(height)]
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            val = grid.get(r, c)
            if val == "#":
                color = 0  # black
            elif val == ".":
                color = 255  # white
            else:
                color = 128  # gray for other markers
            data[r - min_row][c - min_col] = color

    plt.figure(figsize=(6, 6))
    plt.imshow(np.transpose(data), cmap="gray", origin="lower", interpolation="nearest")
    plt.title("Grid view")
    plt.axis("off")
    # plt.gca().invert_yaxis()

    plt.show()


def fill_edges(grid: Grid, polygon: list[tuple[int, int]], fill_char: str):
    # iterate over consecutive pairs on the closed loop
    for prev, curr in zip(polygon, polygon[1:] + polygon[:1]):
        # vertical movement
        if prev[0] != curr[0] and prev[1] == curr[1]:
            row_start = min(prev[0], curr[0])
            row_end = max(prev[0], curr[0])
            col = prev[1]
            for r in range(row_start, row_end + 1):
                grid.set(r, col, fill_char)

        # horizontal movement
        elif prev[1] != curr[1] and prev[0] == curr[0]:
            col_start = min(prev[1], curr[1])
            col_end = max(prev[1], curr[1])
            row = prev[0]
            for c in range(col_start, col_end + 1):
                grid.set(row, c, fill_char)

        else:
            raise ValueError("Only horizontal or vertical edges are supported")


def get_perimeter(coords: list[tuple[int, int]]) -> list[tuple[int, int]]:
    perimeter = []
    # iterate over consecutive pairs
    for prev, curr in zip(coords, coords[1:] + coords[:1]):
        # vertical movement
        if prev[0] != curr[0] and prev[1] == curr[1]:
            row_start = min(prev[0], curr[0])
            row_end = max(prev[0], curr[0])
            col = prev[1]
            for r in range(row_start, row_end + 1):
                perimeter.append((r, col))

        # horizontal movement
        elif prev[1] != curr[1] and prev[0] == curr[0]:
            col_start = min(prev[1], curr[1])
            col_end = max(prev[1], curr[1])
            row = prev[0]
            for c in range(col_start, col_end + 1):
                perimeter.append((row, c))

        else:
            raise ValueError("Only horizontal or vertical edges are supported")
    return perimeter


def rank_coords(
    coords: list[tuple[int, int]],
) -> tuple[list[tuple[int, int]], dict[int, int], dict[int, int]]:
    sorted_rows = sorted({r for r, _ in coords})
    sorted_cols = sorted({c for _, c in coords})

    row_to_row_rank = {v: i for i, v in enumerate(sorted_rows)}
    col_to_col_rank = {v: i for i, v in enumerate(sorted_cols)}

    row_rank_to_row = {i: v for i, v in enumerate(sorted_rows)}
    col_rank_to_col = {i: v for i, v in enumerate(sorted_cols)}

    ranked_coords = [(row_to_row_rank[r], col_to_col_rank[c]) for r, c in coords]
    return ranked_coords, row_rank_to_row, col_rank_to_col


def flood_fill(grid: Grid, row: int, col: int, fill_char: str):
    start_char = grid.get(row, col)

    if start_char == fill_char:
        return

    to_fill = deque()
    to_fill.append((row, col))

    while to_fill:
        r, c = to_fill.popleft()

        # paint all the positions with the same value as the start_char
        if grid.get(r, c) != start_char:
            continue

        grid.set(r, c, fill_char)

        # add neighbors
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr = r + dr
            nc = c + dc
            if grid.is_within_bounds(nr, nc):
                to_fill.append((nr, nc))


def find_largest_rect_inside(grid, ranked_coords, inside_char):
    ranked_max_area = -1
    ranked_max_area_coord1 = None
    ranked_max_area_coord2 = None

    for coord1, coord2 in itertools.combinations(ranked_coords, 2):
        r1, c1 = coord1
        r2, c2 = coord2

        if r1 == r2 and c1 == c2:
            raise Exception("foo")  # does this happen with combinations?

        row_start = min(r1, r2)
        row_end = max(r1, r2)
        col_start = min(c1, c2)
        col_end = max(c1, c2)

        inside = True
        for r in [row_start, row_end]:
            for c in [col_start, col_end]:
                if grid.get(r, c) != inside_char:
                    inside = False
                    break
            if not inside:
                break

        if inside:
            area = (row_end - row_start + 1) * (col_end - col_start + 1)
            if area > ranked_max_area:
                ranked_max_area = area
                ranked_max_area_coord1 = coord1
                ranked_max_area_coord2 = coord2

    return ranked_max_area_coord1, ranked_max_area_coord2


def part2(coords):
    start = time.perf_counter()

    max_area = -1
    max_c1 = None
    max_c2 = None

    for coord1, coord2 in itertools.combinations(coords, 2):
        rect = [
            (coord1[0], coord1[1]),
            (coord1[0], coord2[1]),
            (coord2[0], coord2[1]),
            (coord2[0], coord1[1]),
        ]
        perimeter = coords.copy()  # TODO necessary?

        poly_rect = Polygon(rect)
        poly_perimeter = Polygon(perimeter)

        if poly_rect.intersection(poly_perimeter).area != poly_rect.area:
            continue
        else:
            area = (abs(coord1[0] - coord2[0]) + 1) * (abs(coord1[1] - coord2[1]) + 1)
            if area > max_area:
                max_area = area
                max_c1 = coord1
                max_c2 = coord2

    end = time.perf_counter()
    print(f"part2 elapsed: {end - start:.4f}s")

    print("Max area coords:", max_c1, max_c2)

    assert max_area == 1473551379
    print("Part 2:", max_area)


filename = "day09/example"
filename = "day09/input"

coords = parse(filename)
# part1(coords)
part2(coords)
