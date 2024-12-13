from dataclasses import dataclass
import re


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


def get_solutions(a_x, a_y, b_x, b_y, price_x, price_y):
    """
    Solve system of equations for integer solutions:
    a_x * a + b_x * b = price_x
    a_y * a + b_y * b = price_y
    """

    """
    First example:
    94a + 22b = 8400
    34a + 67b = 5400
    """
    solutions = []

    for a in range(101):
        for b in range(101):
            if (a_x * a + b_x * b == price_x) and (a_y * a + b_y * b == price_y):
                solutions.append((a, b))
    return solutions


def part1(machines: list[Machine]):
    tokens = 0
    for machine in machines:
        a_x, a_y, b_x, b_y, price_x, price_y = machine.a_x, machine.a_y, machine.b_x, machine.b_y, machine.price_x, machine.price_y
        solutions = get_solutions(a_x, a_y, b_x, b_y, price_x, price_y)

        if len(solutions) == 0:
            # print("No solution found")
            continue
        elif len(solutions) == 1:
            a, b = solutions[0]
            # print(a, b)

            tokens += a * COST_A + b * COST_B
        else:
            # assert that there is no more than one solution
            assert False

    print("Part 1:", tokens)


def part2(machines: list[Machine]):
    print("Part 2:", -1)


# filename = "day13/example"
filename = "day13/input"

machines = parse(filename)
part1(machines)
# part2(machines)
