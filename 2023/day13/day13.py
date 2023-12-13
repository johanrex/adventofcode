from dataclasses import dataclass
import math
import re


Grid = list[str]


def parse(filename: str) -> list[Grid]:
    grids = []
    grid = None
    with open(filename) as f:
        for line in f:
            line = line.strip()

            if grid is None:
                grid = []

            if line == "":
                grids.append(grid)
                grid = None
                continue

            grid.append(line)

        if grid is not None:
            grids.append(grid)

        return grids


def flip_grid(grid: Grid) -> Grid:
    new_grid = []
    for c in range(len(grid[0])):
        new_row = ""
        for r in range(len(grid)):
            new_row += grid[r][c]
        new_grid.append(new_row)
    return new_grid


def get_perfect_mirror_idx(grid: Grid) -> int:
    mirror_idx = -1

    for i in range(0, len(grid) - 1):
        if is_perfect_mirror(i, grid):
            mirror_idx = i
            break  # dangerous?
    return mirror_idx


# TODO wtf happens if we have a grid with all identical rows/cols?
def is_perfect_mirror(start_row_idx: int, grid: Grid) -> bool:
    assert start_row_idx >= 0 or start_row_idx < len(grid) - 1

    is_perfect = True

    for offset in range(start_row_idx + 1):
        curr_idx = start_row_idx - offset
        compare_idx = start_row_idx + offset + 1

        if curr_idx < 0:
            break
        if compare_idx >= len(grid):
            break

        if grid[curr_idx] != grid[compare_idx]:
            is_perfect = False
            break

    return is_perfect


def part1(grids: list[Grid]):
    s = 0
    for i, grid in enumerate(grids):
        print("grid", i)
        grid_sum = 0

        # rows
        mirror_idx = get_perfect_mirror_idx(grid)
        if mirror_idx != -1:
            grid_sum = 100 * (mirror_idx + 1)
        else:
            # cols
            grid = flip_grid(grid)

            mirror_idx = mirror_idx = get_perfect_mirror_idx(grid)
            if mirror_idx != -1:
                grid_sum = mirror_idx + 1

        assert grid_sum != 0
        print("grid_sum", grid_sum)
        s += grid_sum

    print("Part 1:", s)


def part2(grids: list[Grid]):
    print("Part 2:", -1)


# filename = "day13/example"
filename = "day13/input"

grids = parse(filename)
part1(grids)
# part2(grids)

# TODO add timer to measure performance
