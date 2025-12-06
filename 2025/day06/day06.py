import math
import re


def parse(filename: str) -> tuple[list[list[str]], list[str]]:
    with open(filename) as f:
        lines = [line.strip("\n") for line in f.readlines()]

    # parse operators from last line
    operator_line = lines[-1]
    operator_idxs = [m.start() for m in re.finditer(r"[+*]", operator_line)]
    operators = [operator_line[idx] for idx in operator_idxs]
    lines.pop()

    # build grid of values
    val_grid = []
    col_start = 0
    for line in lines:
        new_line = []
        for i in range(len(operator_idxs)):
            col_start = operator_idxs[i]

            if i == len(operator_idxs) - 1:
                col_end = len(line)
            else:
                col_end = operator_idxs[i + 1] - 1

            val = line[col_start:col_end]
            new_line.append(val)
        val_grid.append(new_line)

    return val_grid, operators


def parse_p1_vals(vals: list[str]) -> list[int]:
    vals = list(map(int, vals))
    return vals


def parse_p2_vals(vals: list[str]) -> list[int]:
    new_vals = []
    for col_idx in range(len(vals[0])):
        new_val = ""
        for val in vals:
            new_val += val[col_idx]
        new_val = int(new_val)
        new_vals.append(new_val)

    return new_vals


def walk_column_wise(val_grid: list[list[str]], operators: list[str]):
    p1_ans = 0
    p2_ans = 0

    for col_idx in range(len(val_grid[0])):
        operator = operators[col_idx]
        vals = []

        for row_idx in range(len(val_grid)):
            val = val_grid[row_idx][col_idx]
            vals.append(val)

        p1_vals = parse_p1_vals(vals)
        p2_vals = parse_p2_vals(vals)

        if operator == "+":
            p1_ans += sum(p1_vals)
            p2_ans += sum(p2_vals)
        elif operator == "*":
            p1_ans += math.prod(p1_vals)
            p2_ans += math.prod(p2_vals)

    assert p1_ans == 3261038365331
    assert p2_ans == 8342588849093

    print("Part 1:", p1_ans)
    print("Part 2:", p2_ans)


# filename = "day06/example"
filename = "day06/input"

val_grid, operators = parse(filename)
walk_column_wise(val_grid, operators)
