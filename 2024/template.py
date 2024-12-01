import math
import re
import copy
from collections import Counter


def parse(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]
        return lines


def part1(lines):
    print("Part 1:", -1)


def part2(lines):
    print("Part 2:", -1)


filename = "dayX/example"
# filename = "dayX/input"

lines = parse(filename)
part1(lines)
part2(lines)
