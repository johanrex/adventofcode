from dataclasses import dataclass, field
import time
import sys
import math
import re
import copy
from collections import Counter
from typing import List

OP_ADV = 0
OP_BXL = 1
OP_BST = 2
OP_NJZ = 3
OP_BXC = 4
OP_OUT = 5
OP_BDV = 6
OP_CDV = 7


@dataclass
class Computer:
    reg_a: int
    reg_b: int
    reg_c: int
    ip: int
    program: list[int]
    output: list[int] = field(default_factory=list)

    @staticmethod
    def is_literal(operand: int) -> bool:
        return 0 <= operand <= 3

    @staticmethod
    def is_combo(operand: int) -> bool:
        return 4 <= operand <= 6

    def translate_operand(self, operand: int):
        if 0 <= operand <= 3:
            return operand
        elif operand == 4:
            return self.reg_a
        elif operand == 5:
            return self.reg_b
        elif operand == 6:
            return self.reg_c
        else:
            raise ValueError(f"Invalid operand: {operand}")

    def read(self) -> tuple[int, int]:
        if self.ip < len(self.program) - 1:
            return self.program[self.ip], self.program[self.ip + 1]
        else:
            return None, None

    def execute(self):
        while True:
            op, operand = self.read()
            if op is None:
                break

            if op == OP_ADV:
                self.op_adv(operand)
            elif op == OP_BXL:
                self.op_bxl(operand)
            elif op == OP_BST:
                self.op_bst(operand)
            elif op == OP_NJZ:
                self.op_jnz(operand)
            elif op == OP_BXC:
                self.op_bxc(operand)
            elif op == OP_OUT:
                self.op_out(operand)
            elif op == OP_BDV:
                self.op_bdv(operand)
            elif op == OP_CDV:
                self.op_cdv(operand)
            else:
                raise ValueError(f"Invalid opcode: {op}")

    def op_adv(self, operand: int):
        denominator = 2 ** self.translate_operand(operand)
        self.reg_a = self.reg_a // denominator
        self.ip += 2

    def op_bxl(self, operand: int):
        assert Computer.is_literal(operand)

        self.reg_b = self.reg_b ^ self.translate_operand(operand)
        self.ip += 2

    def op_bst(self, operand: int):
        self.reg_b = self.translate_operand(operand) % 8
        self.ip += 2

    def op_jnz(self, operand: int):
        assert Computer.is_literal(operand)
        jumped = None

        if self.reg_a == 0:
            jumped = False
        else:
            jumped = True
            self.ip = operand

        if not jumped:
            self.ip += 2

    def op_bxc(self, operand: int):
        # operand is ignored
        self.reg_b = self.reg_b ^ self.reg_c
        self.ip += 2

    def op_out(self, operand: int):
        output = self.translate_operand(operand) % 8
        self.output.append(output)
        self.ip += 2

    def op_bdv(self, operand: int):
        denominator = 2 ** self.translate_operand(operand)
        self.reg_b = self.reg_a // denominator
        self.ip += 2

    def op_cdv(self, operand: int):
        denominator = 2 ** self.translate_operand(operand)
        self.reg_c = self.reg_a // denominator
        self.ip += 2


def parse(filename: str) -> Computer:
    with open(filename) as f:
        line = f.readline().strip()
        reg_a = int(line.split(":")[1].strip())
        line = f.readline().strip()
        reg_b = int(line.split(":")[1].strip())
        line = f.readline().strip()
        reg_c = int(line.split(":")[1].strip())
        line = f.readline().strip()
        assert line == ""
        line = f.readline().strip()
        program = list(map(int, line.split(":")[1].strip().split(",")))

    computer = Computer(
        reg_a=reg_a,
        reg_b=reg_b,
        reg_c=reg_c,
        ip=0,
        program=program,
    )
    return computer


def test_1():
    computer = Computer(0, 0, 9, 0, [2, 6])
    computer.execute()
    assert computer.reg_b == 1


def test_2():
    computer = Computer(10, 0, 0, 0, [5, 0, 5, 1, 5, 4])
    computer.execute()
    assert computer.output == [0, 1, 2]


def test_3():
    computer = Computer(2024, 0, 0, 0, [0, 1, 5, 4, 3, 0])
    computer.execute()
    assert computer.reg_a == 0
    assert computer.output == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]


def test_4():
    # stupid test?
    computer = Computer(0, 29, 0, 0, [1, 7])
    computer.execute()
    assert computer.reg_b == 26


def test_5():
    computer = Computer(0, 2024, 43690, 0, [4, 0])
    computer.execute()
    assert computer.reg_b == 44354


def part1(computer: Computer):
    print(computer)
    computer.execute()
    assert computer.output == [3, 1, 4, 3, 1, 7, 1, 6, 3]
    output = [str(o) for o in computer.output]
    msg = ",".join(output)

    print("Part 1:", msg)


def part2(computer: Computer):
    initial_program = computer.program.copy()

    start_time = time.perf_counter()

    reg_a_val = None
    for reg_a_val in range(0, sys.maxsize):
        if reg_a_val % 1000000 == 0:
            time_elapsed = time.perf_counter() - start_time
            msg = f"Trying reg_a value: {reg_a_val}. "
            msg += f"Elapsed time: {time_elapsed:.2f}s. "
            msg += f"Vals/s: {reg_a_val / time_elapsed:.2f}."

            print(msg)

        # reset computer
        computer.reg_a = reg_a_val
        computer.reg_b = 0
        computer.reg_c = 0
        computer.ip = 0
        computer.output.clear()

        computer.execute()
        if computer.output == initial_program:
            break

    print("Part 2:", reg_a_val)


# filename = "day17/example"
filename = "day17/input"

computer = parse(filename)

# part1(copy.deepcopy(computer))
part2(copy.deepcopy(computer))
