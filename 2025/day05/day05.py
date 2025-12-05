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


def parse(filename) -> tuple[list[tuple[int, int]], list[int]]:
    ranges = []
    ingredients = []
    with open(filename) as f:
        first_part = True
        while line := f.readline():
            line = line.strip()

            if len(line) == 0:
                first_part = False
                continue

            if first_part:
                # ranges
                start, end = line.split("-")
                ranges.append((int(start), int(end)))
            else:
                # ingredients
                ingredients.append(int(line))
    return ranges, ingredients


def part1(ranges: list[tuple[int, int]], ingredients: list[int]):
    fresh_cnt = 0

    for ingredient in ingredients:
        for start, end in ranges:
            if start <= ingredient <= end:
                fresh_cnt += 1
                break

    print("Part 1:", fresh_cnt)


def merge(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    # sort input on start
    intervals.sort()

    ans = []

    for interval in intervals:
        if len(ans) == 0:
            ans.append(interval)
        else:
            prev_end = ans[-1][1]

            curr_start = interval[0]
            curr_end = interval[1]

            # start new interval
            if curr_start > prev_end:
                ans.append(interval)

            # extend prev interval
            else:
                if curr_end > prev_end:
                    last_interval = ans[-1]
                    start, _ = last_interval
                    ans[-1] = (start, curr_end)

    return ans


def part2(ranges: list[tuple[int, int]]):
    ranges = merge(ranges)

    total_span = 0
    for start, end in ranges:
        total_span += end - start + 1

    print("Part 2:", total_span)


filename = "day05/example"
filename = "day05/input"

ranges, ingredients = parse(filename)

part1(ranges, ingredients)
part2(ranges)
