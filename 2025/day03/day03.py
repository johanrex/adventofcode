from dataclasses import dataclass
import time
import math
import re
import copy
from collections import Counter
import sys
import os
from collections import defaultdict
import itertools

# silly python path manipulation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def parse(filename) -> list[int]:
    data = []
    with open(filename) as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip()
            ints = [int(c) for c in line]
            data.append(ints)
    return data


def part1(data):
    total = 0
    for row in data:
        max_1 = -1
        max_1_idx = -1
        for i in range(len(row) - 1):
            if row[i] > max_1:
                max_1 = row[i]
                max_1_idx = i

        max_2 = -1
        for i in range(max_1_idx + 1, len(row)):
            if row[i] > max_2:
                max_2 = row[i]

        max_num = max_1 * 10 + max_2
        print(max_num)
        total += max_num

    print("Part 1:", total)


def part2(data):
    print("Part 2:", -1)


filename = "day03/example"
filename = "day03/input"

data = parse(filename)
part1(data)
# part2(data)
