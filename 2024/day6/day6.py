from dataclasses import dataclass
import math
import re
import copy
from collections import Counter

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
DIR_IDX_LBLS = ["^", ">", "v", "<"]
dir_idx = 0


@dataclass(frozen=True)
class Pos:
    r: int
    c: int


@dataclass
class Guard:
    pos: Pos
    dir_idx: int


Grid = list[list[str]]
seen = set()


def print_grid(grid: Grid, guard: Guard):
    for r in range(len(grid)):
        row = grid[r].copy()  # copy to avoid modifying the original grid
        for c in range(len(row)):
            if Pos(r, c) == guard.pos:
                row[c] = DIR_IDX_LBLS[guard.dir_idx]

        print("".join(row))


def is_inside_grid(grid: Grid, pos: Pos) -> bool:
    return 0 <= pos.r < len(grid) and 0 <= pos.c < len(grid[0])


def step(grid, guard: Guard) -> bool:
    dir = DIRS[guard.dir_idx]
    g_r, g_c = guard.pos.r, guard.pos.c

    potential_pos = Pos(g_r + dir[0], g_c + dir[1])

    # no step if outside grid
    if not is_inside_grid(grid, potential_pos):
        return False

    # is next cell an obstacle?
    if grid[potential_pos.r][potential_pos.c] == "#":
        # turn right
        guard.dir_idx = turn(guard.dir_idx)
        dir = DIRS[guard.dir_idx]

    # move forward
    g_r += dir[0]
    g_c += dir[1]

    guard.pos = Pos(g_r, g_c)

    return True


def turn(dir_idx: int) -> int:
    return (dir_idx + 1) % 4


def parse(filename: str) -> tuple[Grid, Guard]:
    grid = []
    with open(filename) as f:
        for line in f:
            grid.append([c for c in line.strip()])

    guard_pos: Pos | None = None
    for r in range(len(grid)):
        row = grid[r]
        for c in range(len(row)):
            if row[c] == "^":
                row[c] = "."
                guard_pos = Pos(r, c)
                break
        if guard_pos:
            break

    guard = Guard(guard_pos, 0)

    return grid, guard


def part1(grid, guard):
    print("Initial grid:")
    print_grid(grid, guard)

    seen.add(guard.pos)

    while step(grid, guard):
        # print("")
        # print("After step:")
        # print_grid(grid, guard)

        seen.add(guard.pos)

    print("Part 1:", len(seen))


def part2(grid):
    """
    add obstacle
    if entered obstacte from same direction twice, we have a cycle
    """

    print("Part 2:", -1)


# filename = "day6/example"
filename = "day6/input"

grid, guard = parse(filename)
part1(grid, guard)
part2(grid, guard)
