from dataclasses import dataclass
import math
import re


def parse(filename):
    histories = []
    with open(filename) as f:
        for line in f:
            strs = line.strip().split()
            nrs = [int(s) for s in strs]
            histories.append(nrs)

    return histories


def is_all_zero(nrs):
    for nr in nrs:
        if nr != 0:
            return False
    return True


def difference(nrs):
    diff = [0] * (len(nrs) - 1)
    for i in range(len(nrs) - 1):
        diff[i] = nrs[i + 1] - nrs[i]
    return diff


def extrapolate(history, last=True):
    sequences = []
    sequences.append(history)

    diff = history
    while not is_all_zero(diff):
        diff = difference(diff)
        sequences.append(diff)

    new_val = 0
    for seq in reversed(sequences):
        if last:
            val = seq[-1]
        # print(last_val)
        new_val += val
        pass

    return new_val


def part1(histories):
    s = 0
    for history in histories:
        nr = extrapolate(history)
        s += nr

    # wrong 1974913326
    print("Part 1:", s)


def part2(histories):
    print("Part 2:", histories)


# filename = "day9/example"
filename = "day9/input"

# nrs = list(
#     map(
#         int,
#         "23 43 78 139 250 470 936 1950 4142 8745 18017 35839 68507 125720 221745 376714 617977 981399 1512448 2266875 3310736".split(),
#     )
# )
# print(extrapolate(nrs))


histories = parse(filename)
part1(histories)
# part2(histories)
