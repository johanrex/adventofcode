from dataclasses import dataclass
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


def step(grid, guard: Guard, obstacles_hit: Counter = None) -> bool:
    dir = DIRS[guard.dir_idx]
    g_r, g_c = guard.pos.r, guard.pos.c

    potential_pos = Pos(g_r + dir[0], g_c + dir[1])

    # no step if outside grid
    if not is_inside_grid(grid, potential_pos):
        return False

    # is next cell an obstacle?
    if grid[potential_pos.r][potential_pos.c] == "#":
        if obstacles_hit is not None:
            key = (potential_pos, guard.dir_idx)
            obstacles_hit[key] += 1

            if obstacles_hit[key] > 1:
                return False

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


def part1(grid: Grid, guard: Guard):
    print("Initial grid:")
    print_grid(grid, guard)

    seen.add(guard.pos)

    while step(grid, guard):
        # print("")
        # print("After step:")
        # print_grid(grid, guard)

        seen.add(guard.pos)

    print("Part 1:", len(seen))


def part2(grid: Grid, guard: Guard):
    loop_count = 0

    seen.remove(guard.pos)

    for potential_pos in seen:
        r, c = potential_pos.r, potential_pos.c

        assert potential_pos != guard.pos
        assert grid[r][c] != "#"

        grid_copy = copy.deepcopy(grid)
        guard_copy = copy.deepcopy(guard)
        obstacles_hit = Counter()

        # add an obstacle
        grid_copy[r][c] = "#"

        while step(grid_copy, guard_copy, obstacles_hit):
            pass

        # if we have hit an obstacle more than once, we have a loop
        if obstacles_hit.most_common(1)[0][1] > 1:
            loop_count += 1
            print("Loop count:", loop_count)

    # 1893 too low
    print("Part 2:", loop_count)


# filename = "day6/example"
filename = "day6/input"

grid, guard = parse(filename)
part1(grid, copy.deepcopy(guard))
part2(grid, copy.deepcopy(guard))
