from dataclasses import dataclass
from typing import TextIO
import re


@dataclass
class Instruction:
    n: int
    src: int
    dst: int


def parse_instructions(f: TextIO):
    # "move 1 from 2 to 1"

    pat = re.compile(r"move (\d+) from (\d) to (\d)")
    instructions = []
    while (line := f.readline().strip()) and (len(line) > 0):
        m = re.match(pat, line)
        if not m:
            raise Exception("Unexpected input")

        n = int(m.group(1))
        src = int(m.group(2))
        dst = int(m.group(3))

        instructions.append(Instruction(n=n, src=src, dst=dst))

    return instructions


def parse_setup(f: TextIO):
    #     [D]
    # [N] [C]
    # [Z] [M] [P]
    # 1   2   3

    stacks = []
    first = True
    nr_of_stacks = -1
    while (line := f.readline()) and (len(line.strip()) > 0):
        if first:
            nr_of_stacks = len(line) // 4
            for _ in range(nr_of_stacks):
                stacks.append([])
            first = False

        # is last line with the stack numbers?
        if line.strip().replace(" ", "").isnumeric():
            continue

        for i in range(nr_of_stacks):
            pos = (i * 4) + 1
            if (c := line[pos]) != " ":
                stacks[i].append(c)

    # Reverse stacks for glorious popping later.
    for stack in stacks:
        stack.reverse()

    return stacks


def execute(stacks: list[list[str]], instructions: list[Instruction]):
    for instr in instructions:
        for _ in range(instr.n):
            stack_src = stacks[instr.src - 1]
            stack_dst = stacks[instr.dst - 1]
            item = stack_src.pop()
            stack_dst.append(item)


with open("5/input") as f:
    # with open("5/example") as f:
    stacks = parse_setup(f)
    instructions = parse_instructions(f)
    execute(stacks, instructions)

part1 = ""
for stack in stacks:
    part1 += stack[-1]
print(part1)


pass
