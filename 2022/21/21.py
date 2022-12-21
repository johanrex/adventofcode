from dataclasses import dataclass
from enum import Enum
from operator import add, floordiv, sub, truediv, mul
from typing import Callable
import re

# root: pppw + sjmn
re_operation = re.compile(r"(?P<name>\w+): (?P<operand1>\w+) (?P<operator>[\+\-\*\/]) (?P<operand2>\w+)")
re_value = re.compile(r"(?P<name>\w+): (?P<value>\d+)")


class MonkeyType(Enum):
    VALUE = 1
    OPERATION = 2


class Monkey:
    def __init__(self) -> None:
        self.name: str
        self.type: MonkeyType
        self.value: int
        self.operator: Callable
        self.operand1: str
        self.operand2: str

    def __str__(self) -> str:
        if self.type == MonkeyType.VALUE:
            return f"{self.name}: {self.value}"
        elif self.type == MonkeyType.OPERATION:
            return f"{self.name}: {self.operand1} {self.operator.__name__} {self.operand2}"
        else:
            return "???"


def parse(filename):
    monkeys = []
    with open(filename) as f:
        for line in f:
            line = line.strip()

            if m := re_value.match(line):
                monkey = Monkey()
                monkey.name = m.group("name")
                monkey.type = MonkeyType.VALUE
                monkey.value = int(m.group("value"))
                monkeys.append(monkey)

            elif m := re_operation.match(line):
                monkey = Monkey()
                monkey.name = m.group("name")
                monkey.type = MonkeyType.OPERATION
                monkey.operand1 = m.group("operand1")
                monkey.operand2 = m.group("operand2")

                match m.group("operator"):
                    case "+":
                        monkey.operator = add
                    case "-":
                        monkey.operator = sub
                    case "*":
                        monkey.operator = mul
                    case "/":
                        monkey.operator = floordiv  # truediv/floordiv
                monkeys.append(monkey)
    return monkeys


def eval(monkeys):
    lookup = {m.name: m for m in monkeys}

    unresolveds = [m for m in monkeys if m.type == MonkeyType.OPERATION]

    while len(unresolveds) > 0:

        for unresolved in unresolveds:
            if type(unresolved.operand1) == str and lookup[unresolved.operand1].type == MonkeyType.VALUE:
                unresolved.operand1 = lookup[unresolved.operand1].value

            if type(unresolved.operand2) == str and lookup[unresolved.operand2].type == MonkeyType.VALUE:
                unresolved.operand2 = lookup[unresolved.operand2].value

            # Did we resolve both operands?
            if type(unresolved.operand1) == int and type(unresolved.operand2) == int:
                unresolved.value = unresolved.operator(unresolved.operand1, unresolved.operand2)
                unresolved.type = MonkeyType.VALUE
                unresolved.operand1 = None
                unresolved.operand2 = None
                print("Resolved: ", unresolved.name)

        unresolveds = [m for m in monkeys if m.type == MonkeyType.OPERATION]


filename = "21/input"
monkeys = parse(filename)

eval(monkeys)

monkey = next(m for m in monkeys if m.name == "root")
print(f"Part1. {monkey.name} has value: {monkey.value}")
# [print(m) for m in monkeys]
