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


def print_grid(grid: Grid):
    for row in grid:
        print(row)


def flip_grid(grid: Grid) -> Grid:
    new_grid = []
    for c in range(len(grid[0])):
        new_row = ""
        for r in range(len(grid)):
            new_row += grid[r][c]
        new_grid.append(new_row)
    return new_grid


def get_perfect_mirror_idx(grid: Grid, skip: int = -1) -> int:
    mirror_idx = -1

    for i in range(0, len(grid) - 1):
        if i == skip:
            continue
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


def get_grid_idxs(grid: Grid, skip_row=-1, skip_col=-1) -> tuple[int, int]:
    row_idx = -1
    col_idx = -1

    # rows
    row_idx = get_perfect_mirror_idx(grid, skip_row)
    if row_idx == -1:
        # cols
        grid = flip_grid(grid)
        col_idx = get_perfect_mirror_idx(grid, skip_col)

    return row_idx, col_idx


def get_grid_sum(grid: Grid, skip_row=-1, skip_col=-1) -> int:
    row_idx, col_idx = get_grid_idxs(grid, skip_row, skip_col)

    grid_sum = -1

    if row_idx != -1:
        grid_sum = 100 * (row_idx + 1)

    if col_idx != -1:
        grid_sum = col_idx + 1

    return grid_sum


def smudge(row_idx: int, col_idx: int, grid: Grid) -> Grid:
    # TODO verify that our copy is a deep copy in practice
    grid = grid.copy()

    row = list(grid[row_idx])  # Convert the string to a list

    # flip
    row[col_idx] = "." if row[col_idx] == "#" else "#"

    grid[row_idx] = "".join(
        row
    )  # Convert the list back to a string and replace the row in the grid
    return grid


def part1(grids: list[Grid]):
    s = 0
    for i, grid in enumerate(grids):
        grid_sum = get_grid_sum(grid)
        s += grid_sum

    print("Part 1:", s)


def part2(grids: list[Grid]):
    s = 0
    for i, grid in enumerate(grids):
        # print("grid", i)

        original_row_idx, original_col_idx = get_grid_idxs(grid)

        grid_sum = 0
        found_smudged_grid = False
        for row_idx in range(len(grid)):
            for col_idx in range(len(grid[row_idx])):
                grid_copy = grid.copy()
                smudge_grid = smudge(row_idx, col_idx, grid_copy)
                grid_sum = get_grid_sum(smudge_grid, original_row_idx, original_col_idx)
                if grid_sum == -1:
                    continue

                # print("grid_sum", grid_sum)
                s += grid_sum

                found_smudged_grid = True
                break
            if found_smudged_grid:
                break

        assert grid_sum != 0
    print("Part 2:", s)


# filename = "day13/example"
filename = "day13/input"

grids = parse(filename)
part1(grids)
part2(grids)

# TODO add timer to measure performance
