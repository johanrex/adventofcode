import math
import operator as op


OP_MAPPER = {
    "+": op.add,
    "*": op.mul,
}


def parse1(filename: str) -> tuple[list[list[int]], list[callable]]:
    with open(filename) as f:
        lines = [[c for c in line.strip().split()] for line in f.readlines()]

    operators = lines.pop()

    operators = [OP_MAPPER[op_str] for op_str in operators]

    int_lines = [[int(c) for c in line] for line in lines]

    return int_lines, operators


def parse2(filename: str) -> tuple[list[list[str]], list[callable]]:
    print("Parsing for part 2")

    with open(filename) as f:
        lines = [line.strip("\n") for line in f.readlines()]

    operator_line = lines[-1]
    operator_idxs = []
    operators = []
    for i in range(len(operator_line)):
        if operator_line[i] != " ":
            operator_idxs.append(i)
            operators.append(OP_MAPPER[operator_line[i]])

    lines.pop()

    lines_toks = []
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
        lines_toks.append(new_line)

    return lines_toks, operators


def part1(int_lines: list[list[int]], operators: list[callable]):
    ret = 0

    for col_idx in range(len(int_lines[0])):
        operator = operators[col_idx]
        vals = []

        for row_idx in range(len(int_lines)):
            val = int_lines[row_idx][col_idx]
            vals.append(val)

        if operator == op.add:
            ans = sum(vals)
        elif operator == op.mul:
            ans = math.prod(vals)

        ret += ans
    print("Part 1:", ret)


def p2_calc(vals: list[str], operator: callable) -> int:
    global col_width

    # print(vals, operator)

    new_vals = []
    for col_idx in range(len(vals[0])):
        new_val = ""
        for val in vals:
            new_val += val[col_idx]
        new_val = int(new_val)
        new_vals.append(new_val)

    if operator == op.add:
        ans = sum(new_vals)
    elif operator == op.mul:
        ans = math.prod(new_vals)
    return ans


def part2(lines_toks: list[list[str]], operators: list[callable]):
    ret = 0
    for col_idx in range(len(lines_toks[0])):
        operator = operators[col_idx]
        vals = []

        for row_idx in range(len(lines_toks)):
            val = lines_toks[row_idx][col_idx]
            vals.append(val)

        ans = p2_calc(vals, operator)
        ret += ans

    print("Part 2:", ret)


filename = "day06/example"
filename = "day06/input"

int_lines, operators = parse1(filename)
part1(int_lines, operators)

lines_toks, operators = parse2(filename)
part2(lines_toks, operators)
