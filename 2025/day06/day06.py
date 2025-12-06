import math


def parse2(filename: str) -> tuple[list[list[str]], list[str]]:
    print("Parsing for part 2")

    with open(filename) as f:
        lines = [line.strip("\n") for line in f.readlines()]

    # parse operators from last line
    operator_line = lines[-1]
    operator_idxs = []
    operators = []
    for i in range(len(operator_line)):
        if operator_line[i] != " ":
            operator_idxs.append(i)
            operators.append(operator_line[i])
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


def part1(val_grid: list[list[str]], operators: list[str]):
    ret = 0

    for col_idx in range(len(val_grid[0])):
        operator = operators[col_idx]
        vals = []

        for row_idx in range(len(val_grid)):
            val = val_grid[row_idx][col_idx]
            vals.append(int(val))

        if operator == "+":
            ans = sum(vals)
        elif operator == "*":
            ans = math.prod(vals)

        ret += ans

    # assert ret == 3261038365331
    print("Part 1:", ret)


def p2_calc(vals: list[str], operator: callable) -> int:
    new_vals = []
    for col_idx in range(len(vals[0])):
        new_val = ""
        for val in vals:
            new_val += val[col_idx]
        new_val = int(new_val)
        new_vals.append(new_val)

    if operator == "+":
        ans = sum(new_vals)
    elif operator == "*":
        ans = math.prod(new_vals)

    return ans


def part2(val_grid: list[list[str]], operators: list[str]):
    ret = 0
    for col_idx in range(len(val_grid[0])):
        operator = operators[col_idx]
        vals = []

        for row_idx in range(len(val_grid)):
            val = val_grid[row_idx][col_idx]
            vals.append(val)

        ans = p2_calc(vals, operator)
        ret += ans
    # assert ret == 8342588849093
    print("Part 2:", ret)


filename = "day06/example"
# filename = "day06/input"

val_grid, operators = parse2(filename)

# int_lines, operators = parse1(filename)
part1(val_grid, operators)

part2(val_grid, operators)
