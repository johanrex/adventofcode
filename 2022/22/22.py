from dataclasses import dataclass
from enum import Enum
import re

pat = re.compile(r"(\d+|[RL])")
TURN = 0
STEPS = 1


class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


@dataclass
class Instruction:
    type: int


@dataclass
class InstructionTurn(Instruction):
    turn: str


@dataclass
class InstructionSteps(Instruction):
    steps: int


def parse(filename):
    instructions = []
    with open(filename) as f:
        lines = [line.rstrip("\n") for line in f.readlines()]

        grid = lines[:-2]

        # Assume first line is the longest and pad all to that length
        grid = [line.ljust(len(grid[0])) for line in grid]

        last_line = lines[-1]

        while m := re.match(pat, last_line):
            val = m.group(0)
            if val.isnumeric():
                instructions.append(InstructionSteps(type=STEPS, steps=int(val)))
            else:
                instructions.append(InstructionTurn(type=TURN, turn=val))

            last_line = last_line[m.end() :]
    return grid, instructions


def find_start_tile(grid):
    col = row = 0
    for col in range(len(grid[0])):
        if grid[0][col] == ".":
            break
    return row, col


def find_wraparound(grid, curr_row: int, curr_col: int, direction: Direction) -> tuple[int, int]:
    wrap_row = curr_row
    wrap_col = curr_col

    if direction == Direction.UP:
        wrap_row = len(grid) - 1
        while grid[wrap_row][wrap_col] == " ":
            wrap_row -= 1
    elif direction == Direction.RIGHT:
        wrap_col = 0
        while grid[wrap_row][wrap_col] == " ":
            wrap_col += 1
    elif direction == Direction.DOWN:
        wrap_row = 0
        while grid[wrap_row][wrap_col] == " ":
            wrap_row += 1
    elif direction == Direction.LEFT:
        wrap_col = len(grid[0]) - 1
        while grid[wrap_row][wrap_col] == " ":
            wrap_col -= 1

    assert wrap_row is not None and wrap_col is not None  # TODO performance
    return wrap_row, wrap_col


def is_inside_grid(grid, row, col):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0]) and grid[row][col] != " "


def step_to(row_from: int, col_from: int, steps: int, direction: Direction, grid):
    row_curr = row_from
    col_curr = col_from

    for _ in range(steps):
        row_tmp = row_curr
        col_tmp = col_curr

        if direction == Direction.UP:
            row_tmp = row_curr - 1
        elif direction == Direction.RIGHT:
            col_tmp = col_curr + 1
        elif direction == Direction.DOWN:
            row_tmp = row_curr + 1
        elif direction == Direction.LEFT:
            col_tmp = col_curr - 1

        if is_inside_grid(grid, row_tmp, col_tmp):
            if grid[row_tmp][col_tmp] == ".":
                row_curr = row_tmp
                col_curr = col_tmp
            elif grid[row_tmp][col_tmp] == "#":
                row_tmp = None
                col_tmp = None
            else:
                raise ValueError("Invalid grid value")
        else:
            row_tmp, col_tmp = find_wraparound(grid, row_tmp, col_tmp, direction)
            if grid[row_tmp][col_tmp] == ".":
                row_curr = row_tmp
                col_curr = col_tmp
            elif grid[row_tmp][col_tmp] == "#":
                row_tmp = None
                col_tmp = None
            else:
                raise ValueError("Invalid grid value")

        if row_tmp is None and col_tmp is None:
            break

    return row_curr, col_curr


def walk(grid, instructions):
    direction = Direction.RIGHT
    curr_row, curr_col = find_start_tile(grid)
    for instruction in instructions:
        if instruction.type == TURN and instruction.turn == "R":
            direction = Direction((direction.value + 1) % 4)
        elif instruction.type == TURN and instruction.turn == "L":
            direction = Direction((direction.value - 1) % 4)
        elif instruction.type == STEPS:
            curr_row, curr_col = step_to(curr_row, curr_col, instruction.steps, direction, grid)

    return curr_row, curr_col, direction


def password(row, col, direction):
    return (row + 1) * 1000 + (col + 1) * 4 + direction.value


# filename = "22/example"
filename = "22/input"
grid, instructions = parse(filename)

stop_row, stop_col, stop_direction = walk(grid, instructions)
pwd = password(stop_row, stop_col, stop_direction)
print("Part1:", pwd)
