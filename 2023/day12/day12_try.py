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


def replace_at_idx(s: str, idx: int, c: str):
    if idx == len(s) - 1:
        new_s = s[:idx] + c
    else:
        new_s = s[:idx] + c + s[idx + 1 :]

    return new_s


def get_group_sums_from_state(state) -> tuple[int, ...]:
    lst = []
    group_cnt = 0
    for c in state:
        if c == "#":
            group_cnt += 1
        else:
            if group_cnt > 0:
                lst.append(group_cnt)
                group_cnt = 0

    if group_cnt > 0:
        lst.append(group_cnt)

    return tuple(lst)


def count_arrangements(
    state: str,
    checksums: Checksum,
    state_idx: int,
    checksum_idx: int,
    group_cnt: int = 0,
):
    arrangements = 0

    # the base case
    if state_idx > len(state) - 1:
        if checksum_idx > len(checksums) - 1:
            # assert checksums == get_group_sums_from_state(state)
            return 1
        elif checksum_idx < len(checksums) - 1:
            return 0
        else:
            if group_cnt > 0:
                if group_cnt == checksums[checksum_idx]:
                    # assert checksums == get_group_sums_from_state(state)
                    return 1
                else:
                    return 0
            else:
                return 0
    else:
        if state[state_idx] == "?":
            arrangements += count_arrangements(
                replace_at_idx(state, state_idx, "."),
                checksums,
                state_idx,
                checksum_idx,
                group_cnt,
            )
            arrangements += count_arrangements(
                replace_at_idx(state, state_idx, "#"),
                checksums,
                state_idx,
                checksum_idx,
                group_cnt,
            )
        else:
            if state[state_idx] == ".":
                if group_cnt > 0:
                    if checksums[checksum_idx] != group_cnt:
                        return 0

                    group_cnt = 0
                    checksum_idx += 1

                state_idx += 1
                # while state_idx < len(state) - 1 and state[state_idx] == ".":
                #     state_idx += 1

                arrangements = count_arrangements(
                    state, checksums, state_idx, checksum_idx, group_cnt
                )

            elif state[state_idx] == "#" and checksum_idx <= len(checksums) - 1:
                group_cnt += 1
                if group_cnt > checksums[checksum_idx]:
                    return 0
                else:
                    arrangements += count_arrangements(
                        state, checksums, state_idx + 1, checksum_idx, group_cnt
                    )
            else:
                arrangements = 0

    return arrangements


def part1(problem_infos: list[ProblemInfo]):
    s = 0
    for pi in problem_infos:
        cnt = count_arrangements(pi.corrupt_state, pi.checksums, 0, 0, 0)
        # print(pi.corrupt_state, pi.checksums, f"{cnt} arrangements")
        s += cnt

    print("Part 1:", s)


def part2(problem_infos: list[ProblemInfo]):
    s = 0
    for pi in problem_infos:
        corrupt_state = "?".join([pi.corrupt_state] * 5)
        checksums = pi.checksums * 5

        cnt = count_arrangements(corrupt_state, checksums, 0, 0, 0)
        print(pi.corrupt_state, pi.checksums, f"{cnt} arrangements")
        s += cnt

    print("Part 2:", s)


filename = "day12/example"
# filename = "day12/input"

problem_infos = parse(filename)
part1(problem_infos)
part2(problem_infos)
