from dataclasses import dataclass
import time
import math
import re
import copy
from collections import Counter
import sys
import os
from collections import defaultdict
import operator
from collections.abc import Callable


@dataclass
class Gate:
    wire1: str
    op: Callable[[int, int], int]
    wire2: str
    output_wire: str


def parse(filename: str):
    with open(filename) as f:
        first, second = f.read().strip().split("\n\n")

    wire_values = defaultdict(lambda: None)
    for line in first.split("\n"):
        wire, value = line.strip().split(":")
        wire_values[wire] = int(value)
        # print(wire, wire_values[wire])

    gates = []
    for line in second.split("\n"):
        words = line.split()
        wire1 = words[0]
        op_str = words[1]
        if op_str == "AND":
            op = operator.and_
        elif op_str == "OR":
            op = operator.or_
        elif op_str == "XOR":
            op = operator.xor
        else:
            raise ValueError(f"Invalid op: {op_str}")

        wire2 = words[2]
        output_wire = words[4]

        gates.append(Gate(wire1, op, wire2, output_wire))
        # print(gates[-1])

    return wire_values, gates


def execute(wire_values, gates):
    while len(gates) > 0:
        tmp_gates = []
        for i in range(len(gates)):
            gate = gates[i]
            if wire_values[gate.wire1] is not None and wire_values[gate.wire2] is not None:
                wire_values[gate.output_wire] = gate.op(wire_values[gate.wire1], wire_values[gate.wire2])
            else:
                tmp_gates.append(gate)
        gates = tmp_gates


def get_val(wire_values: defaultdict, wire_startswith: str):
    relevant_wire_values = {k: v for k, v in wire_values.items() if k.startswith(wire_startswith)}
    relevant_wire_names = sorted([name for name in relevant_wire_values.keys()], reverse=True)

    ans = ""
    for wire_name in relevant_wire_names:
        ans += str(relevant_wire_values[wire_name])

    ans = int(ans, 2)
    return ans


def part1(wire_values, gates):
    execute(wire_values, gates)

    ans = get_val(wire_values, "z")

    assert ans == 53190357879014
    print("Part 1:", ans)


def part2(wire_values, gates):
    pass
    # swap


filename = "day24/example"
filename = "day24/input"

wire_values, gates = parse(filename)
part1(copy.deepcopy(wire_values), copy.deepcopy(gates))
part2(copy.deepcopy(wire_values), copy.deepcopy(gates))
