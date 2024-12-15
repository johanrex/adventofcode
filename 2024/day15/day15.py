import math
import re
import copy
from collections import Counter

Pos = tuple[int, int]

DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
DIR_LABELS = [">", "<", "^", "v"]

DIR_MAP = {
    ">": DIRS[0],
    "<": DIRS[1],
    "v": DIRS[2],
    "^": DIRS[3],
}


class Grid:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self._dd = dict()

    def is_within_bounds(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def get(self, row, col, default_value: any = None):
        key = (row, col)
        if key not in self._dd:
            if default_value is not None:
                return default_value
            else:
                raise ValueError(f"Row {row} or col {col} is out of bounds")
        return self._dd[key]

    def set(self, row: int, col: int, value: any, allow_out_of_bounds: bool = False):
        if not allow_out_of_bounds and not self.is_within_bounds(row, col):
            raise ValueError(f"Row {row} or col {col} is out of bounds")

        key = (row, col)
        self._dd[key] = value

    def move(self, row: int, col: int, drow: int, dcol: int, wrap_around: bool = False):
        new_row, new_col = row + drow, col + dcol
        if wrap_around:
            new_row = new_row % self.rows
            new_col = new_col % self.cols

        if self.is_within_bounds(new_row, new_col):
            return new_row, new_col
        else:
            return None, None

    def print_grid(self):
        for row in range(self.rows):
            line = ""
            for col in range(self.cols):
                line += self.get(row, col)
            print(line)


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


def sum_of_box_gps(grid):
    sum = 0
    for r in range(grid.rows):
        for c in range(grid.cols):
            if grid.get(r, c) == "O":
                sum += r * 100 + c
    return sum


def part1(grid, robot_pos: Pos, movements):
    print("Initial state:")
    grid.print_grid()
    print(robot_pos)
    print(movements)

    for m in movements:
        d = DIR_MAP[m]
        steps_to_space = find_empty_space(grid, robot_pos, d)
        if steps_to_space != -1:
            robot_pos = move(grid, robot_pos, d, steps_to_space)

        # print("Move", m)
        # grid.print_grid()
        # print("")

    ans = sum_of_box_gps(grid)

    print("Part 1:", ans)


def part2(data):
    print("Part 2:", -1)


# filename = "day15/example"
filename = "day15/input"

grid, robot_pos, movements = parse(filename)
part1(grid, robot_pos, movements)
# part2(data)
