from collections import Counter
from dataclasses import dataclass
import multiprocessing

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
    current_group_cnt: int = 0,
    cache={},
):
    arrangements = 0

    key = f"{state[state_idx:]},{checksums[checksum_idx:]},{current_group_cnt}"
    if key in cache:
        return cache[key]

    # the base case
    if state_idx > len(state) - 1:
        if checksum_idx > len(checksums) - 1:
            return 1
        elif checksum_idx < len(checksums) - 1:
            return 0
        else:
            if current_group_cnt > 0:
                if current_group_cnt == checksums[checksum_idx]:
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
                current_group_cnt,
                cache,
            )
            arrangements += count_arrangements(
                replace_at_idx(state, state_idx, "#"),
                checksums,
                state_idx,
                checksum_idx,
                current_group_cnt,
                cache,
            )
        else:
            if state[state_idx] == ".":
                if current_group_cnt > 0:
                    if checksums[checksum_idx] != current_group_cnt:
                        return 0

                    current_group_cnt = 0
                    checksum_idx += 1

                state_idx += 1

                arrangements = count_arrangements(
                    state,
                    checksums,
                    state_idx,
                    checksum_idx,
                    current_group_cnt,
                    cache,
                )

            elif state[state_idx] == "#" and checksum_idx <= len(checksums) - 1:
                current_group_cnt += 1
                if current_group_cnt > checksums[checksum_idx]:
                    return 0
                else:
                    arrangements += count_arrangements(
                        state,
                        checksums,
                        state_idx + 1,
                        checksum_idx,
                        current_group_cnt,
                        cache,
                    )
            else:
                arrangements = 0

    cache[key] = arrangements

    return arrangements


def part1(problem_infos: list[ProblemInfo]):
    s = 0
    for pi in problem_infos:
        cnt = count_arrangements(pi.corrupt_state, pi.checksums, 0, 0, 0)
        s += cnt

    print("Part 1:", s)


def part2(problem_infos: list[ProblemInfo]):
    s = 0
    for i, pi in enumerate(problem_infos):
        corrupt_state = "?".join([pi.corrupt_state] * 5)
        checksums = pi.checksums * 5
        cnt = count_arrangements(corrupt_state, checksums, 0, 0, 0)

        print(
            pi.corrupt_state,
            pi.checksums,
            cnt,
            "arrangements. ",
            f"{i}/{len(problem_infos)}",
        )
        s += cnt

    print("Part 2:", s)


def main():
    filename = "day12/example"
    filename = "day12/input"

    problem_infos = parse(filename)
    part1(problem_infos)
    part2(problem_infos)


if __name__ == "__main__":
    main()
