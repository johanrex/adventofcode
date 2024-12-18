import time
import math
import re
import copy
from collections import Counter
import sys
import os

# silly python path manipulation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.grid import Grid


def parse_ints(filename: str):
    nrs = []
    with open(filename) as f:
        for line in f:
            nrs.append(list(map(int, re.findall(r"\d+", line))))
    return nrs


def parse_strs(filename: str):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]
    return lines


def parse_str(filename: str):
    with open(filename) as f:
        text = f.read()

    return text


def part1(data):
    print("Part 1:", -1)


def part2(data):
    print("Part 2:", -1)


filename = "dayX/example"
# filename = "dayX/input"

data = parse_ints(filename)
part1(data)
part2(data)
