from functools import cache
import re
import time
import operator
from itertools import product
from math import log10, floor


@cache
def nr_of_digits(n: int) -> int:
    if n == 0:
        return 1

    return floor(log10(abs(n))) + 1


def operator_concat(a: int, b: int) -> int:
    nr_of_digits_b = nr_of_digits(b)
    return (a * 10**nr_of_digits_b) + b


operators_p1 = [
    operator.add,
    operator.mul,
]

operators_p2 = [*operators_p1, operator_concat]


def parse(filename: str):
    data = []
    with open(filename) as f:
        for line in f:
            nums = list(map(int, re.findall(r"\d+", line)))
            data.append((nums[0], nums[1:]))
    return data


def is_satisfiable(test_value, operands, list_of_operators):
    nr_of_operators = len(operands) - 1

    for ops in product(list_of_operators, repeat=nr_of_operators):
        result = operands[0]
        for i in range(nr_of_operators):
            result = ops[i](result, operands[i + 1])
        if result == test_value:
            return True

    return False


def sum_result_if_satisfiable(data, list_of_operators):
    s = 0
    for test_value, operands in data:
        if is_satisfiable(test_value, operands, list_of_operators):
            s += test_value
    return s


def part1(data):
    s = sum_result_if_satisfiable(data, operators_p1)
    assert s == 3119088655389
    print("Part 1:", s)


def part2(data):
    s = sum_result_if_satisfiable(data, operators_p2)
    assert s == 264184041398847
    print("Part 2:", s)


start_time = time.perf_counter()

# filename = "day7/example"
filename = "day7/input"

data = parse(filename)
part1(data)
part2(data)

end_time = time.perf_counter()
print(f"Total time: {end_time - start_time:.2f} seconds")
