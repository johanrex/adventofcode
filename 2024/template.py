import math
import re
import copy
from collections import Counter


def parse_ints(filename: str):
    nrs = []
    with open(filename) as f:
        for line in f:
            nrs.append(list(map(int, re.findall(r"\d+", line))))
    return nrs


def parse_strs(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]
    return lines


def part1(data):
    print("Part 1:", -1)


def part2(data):
    print("Part 2:", -1)


filename = "dayX/example"
# filename = "dayX/input"

data = parse_ints(filename)
part1(data)
part2(data)
