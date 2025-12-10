from dataclasses import dataclass
import re
from collections import deque
import z3

input_pat = re.compile(r"^\[([^\]]*)\]\s*(.*?)\s*\{([0-9,]+)\}$")

# for part2,
# download and extract z3.
# Set end variable for z3:
# set PATH=C:\z3-4.15.4-x64-win\bin;%PATH%
# uv pip install z3-solver
# The two first machines have z3 input files in day10/z3input folder. I used them as a starting point for the code in part2.


@dataclass()
class Instruction:
    diagram: int
    buttons: list[int]
    joltages: list[int]


def parse(filename: str) -> list[Instruction]:
    manual = []
    with open(filename) as f:
        for line in f:
            m = re.match(input_pat, line)
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

            # print(bin(diagram), [bin(b) for b in buttons])

            joltage = m.group(3)
            joltage = joltage.split(",")
            joltage = [int(j) for j in joltage]

            manual.append(Instruction(diagram, buttons, joltage))
    return manual


def bfs(diagram: int, buttons: list[int]) -> int:
    curr_state = 0
    depth = 0

    q = deque([(curr_state, depth)])
    visited = {(curr_state, -1)}

    while q:
        curr_state, depth = q.popleft()
        if curr_state == diagram:
            return depth

        for b in buttons:
            new_state = curr_state ^ b
            if new_state in visited:
                continue

            visited.add(new_state)
            q.append((new_state, depth + 1))

    return -1


def part1(manual: list[Instruction]):
    total_btn_presses = 0
    for instruction in manual:
        btn_presses = bfs(instruction.diagram, instruction.buttons)
        total_btn_presses += btn_presses

    print("Part 1:", total_btn_presses)


def part2(manual: list[Instruction]):
    total_min_presses = 0

    for idx, instruction in enumerate(manual, 1):
        buttons = instruction.buttons
        joltages = instruction.joltages

        solver = z3.Optimize()

        # one parameter per button
        p = [z3.Int(f"p_{i}") for i in range(len(buttons))]
        for pi in p:
            solver.add(pi >= 0)

        num_counters = len(joltages)
        for k in range(num_counters):
            pos = num_counters - 1 - k
            affected = [p_i for p_i, b in zip(p, buttons) if (b >> pos) & 1]
            solver.add(z3.Sum(affected) == joltages[k])

        total_presses_expr = z3.Sum(p)
        solver.minimize(total_presses_expr)

        # Solve
        result = solver.check()
        if result != z3.sat:
            raise RuntimeError(f"Machine {idx} is unsatisfiable (result: {result})")

        model = solver.model()
        min_presses = model.evaluate(total_presses_expr).as_long()
        total_min_presses += min_presses

        # presses_detail = [model.evaluate(pi).as_long() for pi in p]
        # print(
        #     f"Machine {idx}: min presses = {min_presses}, per-button = {presses_detail}"
        # )

    print("Part 2:", total_min_presses)


# filename = "day10/example"
filename = "day10/input"

manual = parse(filename)
part1(manual)
part2(manual)
