from typing import Generator
import sympy
import math
from datetime import datetime
import time


def parse(filename: str) -> tuple[list[str], list[str], dict[str, str]]:
    with open(filename) as f:
        line = f.readline().strip()
        moves = [c for c in line]

        node_names: list[str] = []
        move_lookup: dict[str, str] = {}

        line = f.readline().strip()
        assert line == ""

        for line in f:
            line = line.strip()

            if line == "":
                break

            node_name = line[0:3]
            left = line[7:10]
            right = line[12:15]

            node_names.append(node_name)

            move_lookup[f"{node_name}L"] = left
            move_lookup[f"{node_name}R"] = right

    return moves, node_names, move_lookup


def get_next_move_generator(moves: list[str]) -> Generator[str, None, None]:
    while True:
        for move in moves:
            yield move


def all_ends_with_z(lst: list[str]) -> bool:
    for x in lst:
        if not x.endswith("Z"):
            return False
    return True


def part2(moves: list[str], node_names: list[str], move_lookup: dict[str, str]) -> None:
    curr_nodes: list[str] = [
        node_name for node_name in node_names if node_name.endswith("A")
    ]

    move_gen = get_next_move_generator(moves)
    steps = 0

    start_time = datetime.now()
    print("Starting at", start_time)

    # prevents division by 0
    time.sleep(0.001)

    while not all_ends_with_z(curr_nodes):
        next_move = next(move_gen)

        keys = [curr + next_move for curr in curr_nodes]
        curr_nodes = [move_lookup[key] for key in keys]

        if steps % 10_000_000 == 0:
            t = (datetime.now() - start_time).total_seconds()
            steps_per_second = steps / t
            print(f"{steps:,}. {steps_per_second:,.0f} steps per second")

        steps += 1

    print("Part 2:", steps)

    end_time = datetime.now()
    print("Ending at", end_time)
    print("Total time:", end_time - start_time)


# filename = "8/example_p2"
filename = "8/input"

moves, node_names, move_lookup = parse(filename)
part2(moves, node_names, move_lookup)
