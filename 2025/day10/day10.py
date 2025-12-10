from dataclasses import dataclass
import time
import math
import re
import copy
from collections import Counter, deque
import sys
import os
from collections import defaultdict
import itertools

# pat = re.compile(r"\[(.+])\](.*)\{([0-9,]+)\}")
pat = re.compile(r"^\[([^\]]*)\]\s*(.*?)\s*\{([0-9,]+)\}$")


@dataclass()
class Instruction:
    diagram: int
    buttons: list[int]


def parse(filename: str) -> list[Instruction]:
    manual = []
    with open(filename) as f:
        for line in f:
            m = re.match(pat, line)
            diagram = m.group(1)
            diagram = diagram.replace(".", "0")
            diagram = diagram.replace("#", "1")

            buttons = m.group(2)
            buttons = buttons.split(" ")
            buttons = [b[1:-1].split(",") for b in buttons]

            new_buttons = []
            for bs in buttons:
                button = "0" * len(diagram)
                bs = [int(b) for b in bs]
                for b in bs:
                    button = button[:b] + "1" + button[b + 1 :]
                new_buttons.append(button)
            buttons = new_buttons

            # paranoia
            s = set([len(b) for b in buttons])
            assert len(s) == 1 and len(diagram) in s

            # print(diagram, buttons)
            diagram = int("".join(diagram), 2)
            buttons = [int("".join(b), 2) for b in buttons]

            manual.append(Instruction(diagram, buttons))

            # print(bin(diagram), [bin(b) for b in buttons])

            joltage = m.group(3)
    return manual


def part1(manual: list[Instruction]):
    def bfs(diagram: int, buttons: list[int]) -> int:
        curr_state = 0
        prev_btn_idx = -1
        prev_states = set()

        q = deque([(curr_state, prev_btn_idx, prev_states)])

        while q:
            curr_state, prev_btn_idx, prev_states = q.popleft()
            if curr_state == diagram:
                return len(prev_states)

            for i, b in enumerate(buttons):
                # don't press the same button twice in a row
                if i == prev_btn_idx:
                    continue

                new_state = curr_state ^ b
                if new_state in prev_states:
                    continue

                new_prev_states = copy.deepcopy(prev_states)
                new_prev_states.add(new_state)
                q.append((new_state, i, new_prev_states))

    total_btn_presses = 0
    for i, instruction in enumerate(manual):
        diagram = instruction.diagram
        buttons = instruction.buttons

        print(
            f"({i + 1}/{len(manual)})",
            "Diagram:",
            bin(diagram),
            "\tButtons:",
            [bin(b) for b in buttons],
            ". ",
            end="",
        )

        btn_presses = bfs(diagram, buttons)
        print("Button presses:", btn_presses)

        total_btn_presses += btn_presses

    print("Part 1:", total_btn_presses)


def part2(manual: list[Instruction]):
    print("Part 2:", -1)


filename = "day10/example"
filename = "day10/input"

manual = parse(filename)
part1(manual)
part2(manual)
