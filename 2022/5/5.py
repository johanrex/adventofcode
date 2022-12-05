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


def execute_part1(stacks: list[list[str]], instructions: list[Instruction]):
    for instr in instructions:
        for _ in range(instr.n):
            stack_src = stacks[instr.src - 1]
            stack_dst = stacks[instr.dst - 1]
            item = stack_src.pop()
            stack_dst.append(item)

    ans = get_answer(stacks)
    assert ans == "QNHWJVJZW"
    return ans


def execute_part2(stacks: list[list[str]], instructions: list[Instruction]):
    for instr in instructions:
        stack_src = stacks[instr.src - 1]
        stack_dst = stacks[instr.dst - 1]

        items = stack_src[-instr.n :]
        stacks[instr.src - 1] = stack_src[: len(stack_src) - instr.n]

        stack_dst.extend(items)

    ans = get_answer(stacks)
    assert ans == "BPCZJLFJW"
    return ans


def get_answer(stacks: list[list[str]]):
    ans = ""
    for stack in stacks:
        ans += stack[-1]
    return ans


filename = "5/input"
# filename = "5/example"

with open(filename) as f:
    stacks = parse_setup(f)
    instructions = parse_instructions(f)

    print(execute_part1(stacks, instructions))

with open(filename) as f:
    stacks = parse_setup(f)
    instructions = parse_instructions(f)

    print(execute_part2(stacks, instructions))
