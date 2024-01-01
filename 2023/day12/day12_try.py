from dataclasses import dataclass
from functools import cache
import itertools
import math
import re
import time
from tqdm import tqdm

Checksum = tuple[int, ...]


@dataclass
class ProblemInfo:
    corrupt_state: str
    checksums: Checksum


def parse(filename: str) -> list[ProblemInfo]:
    problem_infos: list[ProblemInfo] = []
    with open(filename) as f:
        for row in f:
            row = row.strip()
            record, tmp = row.split(" ")
            cs = tmp.split(",")
            checksums = tuple(int(c) for c in cs)

            problem_infos.append(ProblemInfo(record, checksums))
    return problem_infos


def count_arrangements(state: str, checksums: Checksum):
    arrangements = 0

    # the base case
    if state == "" and len(checksums) == 0:
        return 1
    elif state == "" and len(checksums) > 0:
        return 0
    else:
        if (q_idx := state.find("?")) != -1:
            arrangements += count_arrangements(
                state[:q_idx] + "." + state[q_idx + 1 :], checksums
            )
            arrangements += count_arrangements(
                state[:q_idx] + "#" + state[q_idx + 1 :], checksums
            )
        else:
            if state.startswith("."):
                state = state.lstrip(".")
                arrangements = count_arrangements(state, checksums)
            elif state.startswith("#") and len(checksums) > 0:
                broken_cnt = len(state) - len(state.lstrip("#"))
                if broken_cnt == checksums[0]:
                    arrangements += count_arrangements(
                        state[broken_cnt:], checksums[1:]
                    )
                else:
                    return 0
            else:
                return 0

    return arrangements


def part1(problem_infos: list[ProblemInfo]):
    s = 0
    for pi in problem_infos:
        s += count_arrangements(pi.corrupt_state, pi.checksums)

    print("Part 1:", s)


def part2(problem_infos: list[ProblemInfo]):
    s = 0
    for pi in tqdm(problem_infos):
        s += count_arrangements(pi.corrupt_state, pi.checksums)

    print("Part 2:", s)


filename = "day12/example"
# filename = "day12/input"

problem_infos = parse(filename)
part1(problem_infos)

unfolded_problem_infos = []
for pi in problem_infos:
    new_currupt_state = "?".join([pi.corrupt_state] * 5)
    new_checksums = pi.checksums * 5

    unfolded_problem_infos.append(ProblemInfo(new_currupt_state, new_checksums))
part2(unfolded_problem_infos)
