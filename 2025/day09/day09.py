import time

import sys
import os
import itertools
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon

# silly python path manipulation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.grid import Grid


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
