import sys
import os
import time

# silly python path manipulation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.grid import Grid

DIRS = [
    Grid.Pos(0, 1),
    Grid.Pos(0, -1),
    Grid.Pos(1, 0),
    Grid.Pos(-1, 0),
]

DIR_LABELS = [">", "<", "^", "v"]

DIR_MAP = {
    ">": DIRS[0],
    "<": DIRS[1],
    "v": DIRS[2],
    "^": DIRS[3],
}


def parse(filename: str) -> tuple[Grid, Grid.Pos, list[str]]:
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
                robot_pos = Grid.Pos(row, col)

    movements = [m for m in second_section.replace("\n", "").replace("\r", "")]

    return grid, robot_pos, movements


def find_empty_space(grid: Grid, robot_pos: Grid.Pos, d: Grid.Pos):
    # check if there is open space (".") anywhere in the direction before a wall ("#")

    moves = 0
    steps_to_space = -1
    tmp_pos = robot_pos

    while True:
        moves += 1

        tmp_pos = tmp_pos + d

        val = grid.get_by_pos(tmp_pos)
        if val == "#":
            break
        elif val == ".":
            steps_to_space = moves
            break

    return steps_to_space


def move(grid: Grid, robot_pos: Grid.Pos, d: Grid.Pos, steps_to_space: int):
    assert steps_to_space > 0  # check

    if d.row != 0:  # check
        spacepos = Grid.Pos(robot_pos.row + d.row * steps_to_space, robot_pos.col)
        assert grid.get_by_pos(spacepos) == "."
    if d.col != 0:  # check
        spacepos = Grid.Pos(robot_pos.row, robot_pos.col + d.col * steps_to_space)
        assert grid.get_by_pos(spacepos) == "."

    while steps_to_space > 0:
        if d.row != 0:
            dst_pos = Grid.Pos(robot_pos.row + d.row * steps_to_space, robot_pos.col)
            src_pos = Grid.Pos(robot_pos.row + d.row * (steps_to_space - 1), robot_pos.col)

        elif d.col != 0:
            dst_pos = Grid.Pos(robot_pos.row, robot_pos.col + d.col * steps_to_space)
            src_pos = Grid.Pos(robot_pos.row, robot_pos.col + d.col * (steps_to_space - 1))

        assert grid.get_by_pos(dst_pos) == "."
        grid.swap_by_pos(src_pos, dst_pos)

        steps_to_space -= 1

    robot_pos = robot_pos + d
    assert grid.get_by_pos(robot_pos) == "@"  # check
    return robot_pos


def sum_of_box_gps(grid: Grid, target="O"):
    s = 0
    for r in range(grid.rows):
        for c in range(grid.cols):
            if grid.get(r, c) == target:
                s += r * 100 + c
    return s


def part1(grid: Grid, robot_pos: Grid.Pos, movements):
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


def create_wide_grid(grid: Grid) -> tuple[Grid, Grid.Pos]:
    wgrid = Grid(grid.rows, grid.cols * 2, ".")
    robot_pos = None

    for r in range(grid.rows):
        for c in range(grid.cols):
            val = grid.get(r, c)
            if val == "@":
                wgrid.set(r, c * 2, "@")
                wgrid.set(r, c * 2 + 1, ".")

                robot_pos = Grid.Pos(r, c * 2)
            elif val == "O":
                wgrid.set(r, c * 2, "[")
                wgrid.set(r, c * 2 + 1, "]")
            elif val == "#":
                wgrid.set(r, c * 2, "#")
                wgrid.set(r, c * 2 + 1, "#")

    assert robot_pos is not None
    return wgrid, robot_pos


def find_affected_grid_positions(grid: Grid, robot_pos: Grid.Pos, d: Grid.Pos) -> set[Grid.Pos]:
    # find positions to push in the direction d.
    # a box is two positions wide.

    q = [robot_pos]
    affected_grid_pos = set([robot_pos])

    while len(q) > 0:
        affected_pos = q.pop(0)
        next_pos = affected_pos + d
        val = grid.get_by_pos(next_pos)

        if val == "#":
            # if we hit a wall we can't move anything.
            # we indicate this by returning None
            affected_grid_pos = None
            break

        if val == "[":
            first = next_pos
            second = Grid.Pos(next_pos.row, next_pos.col + 1)

            q.append(first)
            q.append(second)

            affected_grid_pos.add(first)
            affected_grid_pos.add(second)
        elif val == "]":
            first = Grid.Pos(next_pos.row, next_pos.col - 1)
            second = next_pos

            q.append(first)
            q.append(second)

            affected_grid_pos.add(first)
            affected_grid_pos.add(second)

    return affected_grid_pos


def part2(grid: Grid, movements: list[str]):
    grid, robot_pos = create_wide_grid(grid)

    # print("Movements:")
    # print(movements)

    # print("Initial state:")
    # grid.print_grid()
    # print("")

    for movement_idx, m in enumerate(movements):
        d = DIR_MAP[m]
        if d.col != 0:  # we can reuse function from part 1
            steps_to_space = find_empty_space(grid, robot_pos, d)
            if steps_to_space != -1:
                robot_pos = move(grid, robot_pos, d, steps_to_space)
        else:
            # we are moving up or down

            # find positions of robot + boxes involved in push
            affected_grid_pos = find_affected_grid_positions(grid, robot_pos, d)
            if affected_grid_pos is None:
                continue
            else:
                if d.row == -1:
                    affected_grid_pos = sorted(affected_grid_pos)
                else:
                    affected_grid_pos = sorted(affected_grid_pos, reverse=True)

                for src_pos in affected_grid_pos:
                    dst_pos = src_pos + d

                    assert grid.get_by_pos(dst_pos) == "."

                    grid.swap_by_pos(src_pos, dst_pos)

            robot_pos = robot_pos + d

        # print(f"Move {m}. ({movement_idx=})")
        # grid.print_grid()
        # print("")

    ans = sum_of_box_gps(grid, target="[")
    assert ans == 1399772
    print("Part 2:", ans)


start_time = time.perf_counter()

# filename = "day15/example"
filename = "day15/input"

grid, robot_pos, movements = parse(filename)
part1(grid, robot_pos, movements)
grid, robot_pos, movements = parse(filename)
part2(grid, movements)

end_time = time.perf_counter()
print(f"Total time: {end_time - start_time} seconds")
