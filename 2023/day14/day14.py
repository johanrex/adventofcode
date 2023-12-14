from dataclasses import dataclass, field
import math
import re
from tqdm import tqdm

NORTH = 0
WEST = 1
SOUTH = 2
EAST = 3
DIRECTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)]

GridItem = tuple[int, int, str]


@dataclass
class Grid:
    n_rows: int
    n_cols: int

    _lookup: dict[tuple[int, int], str] = field(default_factory=dict)

    def get_items(self) -> list[GridItem]:
        items = []
        for k, v in self._lookup.items():
            items.append((k[0], k[1], v))

        return items

    def is_empty(self, row: int, col: int) -> bool:
        key = (row, col)
        return key not in self._lookup

    def get_at(self, row: int, col: int) -> str:
        key = (row, col)

        if key in self._lookup:
            return self._lookup[key]
        else:
            return "."

    def set_at(self, row: int, col: int, c: str):
        key = (row, col)
        assert c != "."
        assert key not in self._lookup
        self._lookup[key] = c

    def remove_at(self, row: int, col: int):
        key = (row, col)
        assert key in self._lookup
        del self._lookup[key]


def parse(filename: str) -> Grid:
    items: list[GridItem] = []
    n_rows = 0
    n_cols = 0

    with open(filename) as f:
        for line in f:
            line = line.strip()

            line_stones = [
                (n_rows, col_idx, c) for col_idx, c in enumerate(line) if c != "."
            ]
            items.extend(line_stones)

            n_cols = len(line)
            n_rows += 1

    grid = Grid(n_rows, n_cols)
    for grid_item in items:
        row, col, c = grid_item
        grid.set_at(row, col, c)

    return grid


def print_grid(grid: Grid):
    rows: list[list[str]] = []
    for _ in range(grid.n_rows):
        rows.append(["."] * grid.n_cols)

    for row in range(grid.n_rows):
        for col in range(grid.n_cols):
            rows[row][col] = grid.get_at(row, col)

    for r in rows:
        s = "".join(r)
        print(s)

    print("")


def can_step(grid: Grid, rock: GridItem, direction: int) -> bool:
    row, col, _ = rock

    d_row, d_col = DIRECTIONS[direction]

    row_dest = row + d_row
    col_dest = col + d_col
    if (0 <= row_dest < grid.n_rows) and (0 <= col_dest < grid.n_cols):
        return grid.get_at(row_dest, col_dest) == "."
    else:
        return False


def step(grid: Grid, rock: GridItem, direction) -> GridItem:
    assert can_step(grid, rock, direction)

    row, col, c = rock
    d_row, d_col = DIRECTIONS[direction]
    row_dest = row + d_row
    col_dest = col + d_col

    if (0 <= row_dest < grid.n_rows) and (0 <= col_dest < grid.n_cols):
        t = grid.get_at(row_dest, col_dest)
        if t == ".":
            grid.remove_at(row, col)
            grid.set_at(row_dest, col_dest, c)
            rock = (row_dest, col_dest, c)

    return rock


def tilt(grid: Grid, direction) -> Grid:
    # TODO verify that they are sorted
    all_rocks = grid.get_items()

    if direction == NORTH or direction == SOUTH:
        for col_idx in range(grid.n_cols):
            round_rocks_affected = [
                (r, c, t) for r, c, t in all_rocks if c == col_idx and t == "O"
            ]

            if direction == NORTH:
                round_rocks_affected.sort()

            else:
                round_rocks_affected.sort(reverse=True)

            for rock in round_rocks_affected:
                while can_step(grid, rock, direction):
                    rock = step(grid, rock, direction)
    elif direction == WEST or direction == EAST:
        for row_idx in range(grid.n_rows):
            round_rocks_affected = [
                (r, c, t) for r, c, t in all_rocks if r == row_idx and t == "O"
            ]

            if direction == WEST:
                round_rocks_affected.sort()

            else:
                round_rocks_affected.sort(reverse=True)

            for rock in round_rocks_affected:
                while can_step(grid, rock, direction):
                    rock = step(grid, rock, direction)
    return grid


def cycle(grid: Grid) -> Grid:
    tilt(grid, NORTH)
    tilt(grid, WEST)
    tilt(grid, SOUTH)
    tilt(grid, EAST)
    return grid


def calc_total_load(grid: Grid) -> int:
    total_load = 0
    for row in range(grid.n_rows):
        for col in range(grid.n_cols):
            if grid.get_at(row, col) == "O":
                total_load += grid.n_rows - row
    return total_load


def part1(grid: Grid):
    tilt(grid, NORTH)
    total_load = calc_total_load(grid)

    assert 109424 == total_load
    print("Part 1:", total_load)


def part2(grid: Grid):
    # nr_of_cycles = 3
    # nr_of_cycles = 1_000_000_000
    total_loads = []
    nr_of_cycles = 120
    # for i in tqdm(range(nr_of_cycles)):
    for i in tqdm(range(1, nr_of_cycles + 1)):
        cycle(grid)
        total_load = calc_total_load(grid)
        total_loads.append(total_load)
        # print(f"cycle {i}: total_load {total_load}")

    candidates = sorted(set(total_loads[-10:]))
    print("one of these should do:", candidates)

    # total_load = calc_total_load(grid)

    # assert 102509 == total_load
    # print("Part 2:", total_load)


filename = "day14/example"
filename = "day14/input"

grid = parse(filename)
# part1(grid)
part2(grid)
