from dataclasses import dataclass
import itertools
import math
import re


def parse(filename):
    with open(filename) as f:
        rows = [row.strip() for row in f.readlines()]
        return rows


def validate(state, checksums):
    checksums_offset = 0
    checksum_cnt = 0
    dmg_cnt = 0
    for s in state:
        if s == ".":
            if checksum_cnt != dmg_cnt:
                return False

            dmg_cnt = 0
            continue
        elif s == "#":
            if dmg_cnt == 0:
                if checksum_cnt == len(checksums):
                    return False

                checksum_cnt = checksums[checksums_offset]
                checksums_offset += 1

            dmg_cnt += 1
        else:
            # TODO optimize away this check
            raise Exception("Unknown state: " + s)

    if checksum_cnt != dmg_cnt:
        return False

    return True


def get_valid_state_cnt(corrupt_state, checksums):
    corrupt_cnt = corrupt_state.count("?")
    elements = ["#", "."]
    gen = itertools.product(elements, repeat=corrupt_cnt)

    valid_cnt = 0
    while items := next(gen, None):
        # TODO may not need to copy
        state_candidate = corrupt_state.copy()
        item_offset = 0
        for i, c in enumerate(corrupt_state):
            if c == "?":
                state_candidate[i] = items[item_offset]
                item_offset += 1

        if validate(state_candidate, checksums):
            valid_cnt += 1

    return valid_cnt


def part1(rows):
    s = 0
    for row in rows:
        print(row, end="")

        record, checksums = row.split(" ")
        record = [c for c in record]
        checksums = checksums.split(",")
        checksums = [int(c) for c in checksums]

        n = get_valid_state_cnt(record, checksums)
        print(" -> ", n)
        s += n

    print("Part 1:", s)


def part2(rows):
    print("Part 2:", rows)


filename = "day12/example"
# filename = "day12/input"

rows = parse(filename)
part1(rows)
# part2(rows)
