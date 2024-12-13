from dataclasses import dataclass
import re
from sympy import solve, symbols, Eq


COST_A = 3
COST_B = 1


@dataclass
class Machine:
    a_x: int
    a_y: int
    b_x: int
    b_y: int
    price_x: int
    price_y: int


def parse(filename: str) -> list[Machine]:
    machines = []
    with open(filename) as f:
        while line := f.readline():
            line = line.strip()

            if len(line) == 0:
                continue
            else:
                a_x, a_y = list(map(int, re.findall(r"\d+", line)))
                b_x, b_y = list(map(int, re.findall(r"\d+", f.readline().strip())))
                price_x, price_y = list(map(int, re.findall(r"\d+", f.readline().strip())))

                machine = Machine(a_x, a_y, b_x, b_y, price_x, price_y)
                machines.append(machine)

    return machines


def get_solution(a_x, a_y, b_x, b_y, price_x, price_y):
    """
    Solve system of equations for integer solutions:
    a_x * a + b_x * b = price_x
    a_y * a + b_y * b = price_y
    """
    a, b = symbols("a, b", integer=True)
    system = [Eq(a_x * a + b_x * b, price_x), Eq(a_y * a + b_y * b, price_y)]
    set_of_solutions = solve(system, [a, b], dict=True)

    if len(set_of_solutions) == 0:
        return None, None
    elif len(set_of_solutions) == 1:
        a = set_of_solutions[0][a]
        b = set_of_solutions[0][b]

        return a, b
    else:
        assert False


def count_tokens(machines: list[Machine]):
    tokens = 0
    for machine in machines:
        a_x, a_y, b_x, b_y, price_x, price_y = machine.a_x, machine.a_y, machine.b_x, machine.b_y, machine.price_x, machine.price_y
        a, b = get_solution(a_x, a_y, b_x, b_y, price_x, price_y)

        if a is None and b is None:
            continue

        tokens += a * COST_A + b * COST_B

    return tokens


def part2(machines: list[Machine]):
    print("Part 2:", -1)


# filename = "day13/example"
filename = "day13/input"

machines = parse(filename)

tokens = count_tokens(machines)
print("Part 1:", tokens)

for m in machines:
    m.price_x += 10000000000000
    m.price_y += 10000000000000

tokens = count_tokens(machines)
print("Part 2:", tokens)
