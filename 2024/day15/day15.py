import sys
import os

# silly python path manipulation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.grid import Grid

Pos = tuple[int, int]

DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
DIR_LABELS = [">", "<", "^", "v"]

DIR_MAP = {
    ">": DIRS[0],
    "<": DIRS[1],
    "v": DIRS[2],
    "^": DIRS[3],
}


def parse(filename: str):
    row = 0

    lines = []
    first_section = True
    with open(filename) as f:
        content = f.read()

    first_section, second_section = content.strip().split("\n\n")

    first_section = first_section.split("\n")
    rows = len(first_section)
    cols = len(first_section[0])
    grid = Grid(rows, cols)

    robot_pos = None

    for row, line in enumerate(first_section):
        line = line.strip()

        for col, val in enumerate(line):
            grid.set(row, col, val)
            if val == "@":
                assert robot_pos is None
                robot_pos = (row, col)

    movements = [m for m in second_section.replace("\n", "").replace("\r", "")]

    return grid, robot_pos, movements


def find_empty_space(grid: Grid, robot_pos: Pos, d: Pos):
    # check if there is open space (".") anywhere in the direction before a wall ("#")

    moves = 0
    steps_to_space = -1
    d_r, d_c = d
    tmp_r, tmp_c = robot_pos

    while True:
        moves += 1
        tmp_r, tmp_c = tmp_r + d_r, tmp_c + d_c

        val = grid.get(tmp_r, tmp_c)
        if val == "#":
            break
        elif val == ".":
            steps_to_space = moves
            break

    return steps_to_space


def move(grid: Grid, robot_pos: Pos, d: Pos, steps_to_space: int):
    d_r, d_c = d
    robot_r, robot_c = robot_pos

    assert steps_to_space > 0  # check
    if d_r != 0:  # check
        assert grid.get(robot_r + d_r * steps_to_space, robot_c) == "."
    if d_c != 0:  # check
        assert grid.get(robot_r, robot_c + d_c * steps_to_space) == "."

    while steps_to_space > 0:
        if d_r != 0:
            dst_r = robot_r + d_r * steps_to_space
            dst_c = robot_c

            src_r = robot_r + d_r * (steps_to_space - 1)
            src_c = robot_c

        elif d_c != 0:
            dst_r = robot_r
            dst_c = robot_c + d_c * steps_to_space

            src_r = robot_r
            src_c = robot_c + d_c * (steps_to_space - 1)

        val_to_move = grid.get(src_r, src_c)
        grid.set(src_r, src_c, ".")
        grid.set(dst_r, dst_c, val_to_move)

        steps_to_space -= 1

    robot_pos = (robot_r + d_r, robot_c + d_c)
    assert grid.get(robot_pos[0], robot_pos[1]) == "@"  # check
    return robot_pos


def sum_of_box_gps(grid, target="O"):
    sum = 0
    for r in range(grid.rows):
        for c in range(grid.cols):
            if grid.get(r, c) == target:
                sum += r * 100 + c
    return sum


def part1(grid, robot_pos: Pos, movements):
    # print("Initial state:")
    # grid.print_grid()
    # print(movements)

    for m in movements:
        d = DIR_MAP[m]
        steps_to_space = find_empty_space(grid, robot_pos, d)
        if steps_to_space != -1:
            robot_pos = move(grid, robot_pos, d, steps_to_space)

        # print("Move", m)
        # grid.print_grid()
        # print("")

    ans = sum_of_box_gps(grid)
    assert ans == 1413675

    print("Part 1:", ans)


def create_wide_grid(grid: Grid) -> tuple[Grid, Pos]:
    wgrid = Grid(grid.rows, grid.cols * 2)
    robot_pos = None

    for r in range(grid.rows):
        for c in range(grid.cols):
            val = grid.get(r, c)
            if val == "@":
                wgrid.set(r, c * 2, "@")
                wgrid.set(r, c * 2 + 1, ".")

                robot_pos = (r, c * 2)
            elif val == "O":
                wgrid.set(r, c * 2, "[")
                wgrid.set(r, c * 2 + 1, "]")
            else:
                wgrid.set(r, c * 2, val)
                wgrid.set(r, c * 2 + 1, val)

    assert robot_pos is not None
    return wgrid, robot_pos


def find_affected_grid_positions(grid: Grid, robot_pos: Pos, d: Pos):
    # find positions to push in the direction d.
    # a box is two positions wide.

    d_r, d_c = d

    q = [robot_pos]
    affected_grid_pos = set([robot_pos])

    while len(q) > 0:
        affected_grid_r, affected_grid_c = q.pop(0)
        next_grid_r, next_grid_c = affected_grid_r + d_r, affected_grid_c + d_c
        val = grid.get(next_grid_r, next_grid_c)

        if val == "#":
            # if we hit a wall we can't move anything.
            # we indicate this by returning None
            affected_grid_pos = None
            break

        if val == "[":
            q.append((next_grid_r, next_grid_c))
            q.append((next_grid_r, next_grid_c + 1))

            affected_grid_pos.add((next_grid_r, next_grid_c))
            affected_grid_pos.add((next_grid_r, next_grid_c + 1))
        elif val == "]":
            q.append((next_grid_r, next_grid_c))
            q.append((next_grid_r, next_grid_c - 1))

            affected_grid_pos.add((next_grid_r, next_grid_c - 1))
            affected_grid_pos.add((next_grid_r, next_grid_c))

    return affected_grid_pos


def part2(grid: Grid, movements):
    grid, robot_pos = create_wide_grid(grid)

    # print("Movements:")
    # print(movements)

    # print("Initial state:")
    # grid.print_grid()
    # print("")

    for movement_idx, m in enumerate(movements):
        d = DIR_MAP[m]
        d_r, d_c = d
        if d_c != 0:  # we can reuse function from part 1
            steps_to_space = find_empty_space(grid, robot_pos, d)
            if steps_to_space != -1:
                robot_pos = move(grid, robot_pos, d, steps_to_space)
        else:
            # we are pushing up or down

            # find boxes involved in push
            affected_grid_pos = find_affected_grid_positions(grid, robot_pos, d)
            if affected_grid_pos is None:
                continue
            else:
                if d_r == -1:
                    affected_grid_pos = sorted(affected_grid_pos, key=lambda x: x[0])
                else:
                    affected_grid_pos = sorted(affected_grid_pos, key=lambda x: x[0], reverse=True)

                for src_pos in affected_grid_pos:
                    src_r, src_c = src_pos
                    dst_r, dst_c = src_r + d_r, src_c

                    assert grid.get(dst_r, dst_c) == "."

                    grid.swap(src_r, src_c, dst_r, dst_c)

            robot_pos = (robot_pos[0] + d_r, robot_pos[1])

        # print(f"Move {m}. ({movement_idx=})")
        # grid.print_grid()
        # print("")

    ans = sum_of_box_gps(grid, target="[")
    assert ans == 1399772
    print("Part 2:", ans)


# filename = "day15/example"
filename = "day15/input"

grid, robot_pos, movements = parse(filename)
part1(grid, robot_pos, movements)
grid, robot_pos, movements = parse(filename)
part2(grid, movements)
