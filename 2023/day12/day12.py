from dataclasses import dataclass
import itertools
import math
import re
import time


@dataclass
class ProblemInfo:
    corrupt_state: list[str]
    checksums: list[int]


def parse(filename):
    problem_infos: list[ProblemInfo] = []
    with open(filename) as f:
        for row in f:
            row = row.strip()
            record, checksums = row.split(" ")
            record = [c for c in record]
            checksums = checksums.split(",")
            checksums = [int(c) for c in checksums]

            problem_infos.append(ProblemInfo(record, checksums))
    return problem_infos


def create_regex_from_checksums(checksums):
    optional_sep_part = r"\.*"
    mandatory_sep_part = r"\.+"
    re_str = optional_sep_part
    for cnt in checksums:
        re_str += "#" * cnt
        re_str += mandatory_sep_part

    # remove last mandatory sep part
    re_str = re_str[: -len(mandatory_sep_part)]

    # add optional sep part
    re_str += optional_sep_part

    # add EOL
    re_str += "$"

    # print("using this re:", re_str)
    return re.compile(re_str)


def is_valid(state, re):
    return re.match("".join(state)) is not None


def get_valid_state_cnt(corrupt_state, checksums):
    regex = create_regex_from_checksums(checksums)

    corrupt_cnt = corrupt_state.count("?")
    elements = ["#", "."]
    gen = itertools.product(elements, repeat=corrupt_cnt)

    # print("".join(corrupt_state), ",".join([str(c) for c in checksums]))
    state_candidate = corrupt_state.copy()
    valid_cnt = 0
    while items := next(gen, None):
        item_offset = 0
        for i, c in enumerate(corrupt_state):
            if c == "?":
                state_candidate[i] = items[item_offset]
                item_offset += 1

        if is_valid(state_candidate, regex):
            # print("\t", "".join(state_candidate))
            valid_cnt += 1

    return valid_cnt


def unfold(corrupt_state: list[str], checksums: list[int]):
    new_corrupt_state = [*corrupt_state, "?"] * 5
    new_corrupt_state.pop()  # remove last ?

    new_checksums = checksums * 5
    return new_corrupt_state, new_checksums


def part1(problem_infos):
    start_time = time.time()

    s = 0
    for problem_info in problem_infos:
        n = get_valid_state_cnt(problem_info.corrupt_state, problem_info.checksums)
        s += n

    print("Part 1:", s)
    print("Time elapsed:", time.time() - start_time)


def part2(problem_infos):
    start_time = time.time()

    s = 0
    for problem_info in problem_infos:
        # unfold
        corrupt_state, checksums = unfold(
            problem_info.corrupt_state, problem_info.checksums
        )

        n = get_valid_state_cnt(corrupt_state, checksums)
        s += n

    print("Part 2:", s)
    print("Time elapsed:", time.time() - start_time)


# filename = "day12/example"
filename = "day12/input"

problem_infos = parse(filename)
part1(problem_infos)


# part2(problem_infos)
