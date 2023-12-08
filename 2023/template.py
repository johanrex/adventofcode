from dataclasses import dataclass
import math
import re


def parse(filename):
    with open(filename) as f:
        lines = [line for line in f.readline().strip()]
        return lines


def part1(lines):
    print("Part 1:", lines)


def part2(lines):
    print("Part 2:", lines)


filename = "dayX/example"
# filename = "dayX/input"

lines = parse(filename)
part1(lines)
part2(lines)
