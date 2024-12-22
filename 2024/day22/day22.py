from functools import cache
import time
import math
import re
import copy
from collections import Counter
import sys
import os
from collections import defaultdict
import pandas as pd

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
        # print(f"{original} -> {secret}.")

    assert s == 13429191512
    print("Part 1:", s)


def part2(secrets):
    all_sequences_of_changes = set()

    monkey_secrets = dict()
    for monkey_id, secret in enumerate(secrets):
        # store tuple of (secret, ones_digit, diff)
        batch = []
        batch.append((secret, secret % 10, None))
        # print(batch[-1])

        for i in range(2000):
            secret = evolve(secret)

            ones_digit = secret % 10
            diff = ones_digit - batch[-1][1]

            batch.append((secret, ones_digit, diff))
            # print(batch[-1])

            if i >= 3:
                all_sequences_of_changes.add((batch[-4][2], batch[-3][2], batch[-2][2], batch[-1][2]))

        # remove first element
        batch = batch[1:]

        monkey_secrets[monkey_id] = batch

    all_total_banana_counts = []

    for sequence_of_changes in all_sequences_of_changes:
        # get banana count for current sequence
        total_banana_count = 0
        for monkey_id, batch in monkey_secrets.items():
            for i in range(3, len(batch)):
                if (batch[i - 3][2], batch[i - 2][2], batch[i - 1][2], batch[i][2]) == sequence_of_changes:
                    banana_count = batch[i][1]
                    total_banana_count += banana_count
                    break
        all_total_banana_counts.append(total_banana_count)

    max_bananas = max(all_total_banana_counts)

    # df = pd.DataFrame(batch, columns=["secret", "ones_digit", "diff"]).astype("Int64")
    # print(df)

    print("Part 2:", max_bananas)


filename = "day22/example"
filename = "day22/input"

secrets = parse(filename)
# part1(secrets)
part2(secrets)
# part2([123])
