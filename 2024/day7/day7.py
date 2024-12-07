import math
import re
import copy
from collections import Counter
import operator
from itertools import product

operators = [
    operator.add,
    operator.mul,
]


def parse(filename: str):
    data = []
    with open(filename) as f:
        for line in f:
            nums = list(map(int, re.findall(r"\d+", line)))
            data.append((nums[0], nums[1:]))
    return data


def is_satisfiable(test_value, operands):
    nr_of_operators = len(operands) - 1

    for ops in product(operators, repeat=nr_of_operators):
        result = operands[0]
        for i in range(nr_of_operators):
            result = ops[i](result, operands[i + 1])
        if result == test_value:
            return True

    return False


def part1(data):
    s = 0
    for eq in data:
        test_value = eq[0]
        operands = eq[1]

        if is_satisfiable(test_value, operands):
            s += test_value

    print("Part 1:", s)


def part2(data):
    print("Part 2:", -1)


# filename = "day7/example"
filename = "day7/input"

data = parse(filename)
part1(data)
# part2(data)
