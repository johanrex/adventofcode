import time
import math
import re
import copy
from collections import Counter
import sys
import os
from collections import defaultdict

# silly python path manipulation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import utils.parse_utils as parse_utils


def parse(filename: str):
    ints = []
    with open(filename) as f:
        for line in f:
            ints.append(int(line.strip()))
    return ints


def evolve(secret: int) -> int:
    tmp = secret * 64
    secret ^= tmp  # mix
    secret %= 16777216  # prune
    tmp = secret // 32
    secret ^= tmp  # mix
    secret %= 16777216  # prune
    tmp = secret * 2048
    secret ^= tmp  # mix
    secret %= 16777216  # prune

    return secret


def part1(secrets):
    s = 0
    for secret in secrets:
        original = secret
        for _ in range(2000):
            secret = evolve(secret)
        s += secret
        print(f"{original} -> {secret}.")

    print("Part 1:", s)


filename = "day22/example"
filename = "day22/input"

secrets = parse(filename)
part1(secrets)
