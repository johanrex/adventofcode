import math
import re
import copy
from collections import Counter, defaultdict


def parse_input(filename: str):
    with open(filename) as f:
        text = f.read()

    rules_section, updates_section = text.strip().split("\n\n")

    # Parse rules into pairs
    rules = []
    for line in rules_section.split("\n"):
        before, after = map(int, line.split("|"))
        rules.append((before, after))

    # Parse orders into lists of numbers
    updates = []
    for line in updates_section.split("\n"):
        update = [int(x) for x in line.split(",")]
        assert len(update) % 2 == 1
        updates.append(update)

    return rules, updates


def build_graph(rules):
    rule_graph = defaultdict(set)
    for before, after in rules:
        rule_graph[before].add(after)
    return rule_graph


def is_valid_order(update, rule_graph):
    # are all rules ok?
    seen = set()
    for num in update:
        for prev in seen:
            if num in rule_graph[prev]:
                continue
            else:
                return False
        seen.add(num)
    return True


def part1(rules, updates_in_order):
    s = 0

    print("Updates in order:")
    for update in updates_in_order:
        middle = update[len(update) // 2]
        s += middle
        print(update, "->", middle)

    # assert s == 5991
    print("Part 1:", s)


def part2(rules, updates_not_in_order):
    for update in updates_not_in_order:
        print(update)

    print("Part 2:", -1)


filename = "day5/example"
# filename = "day5/input"

rules, updates = parse_input(filename)

rule_graph = build_graph(rules)
updates_in_order = []
updates_not_in_order = []
for update in updates:
    if is_valid_order(update, rule_graph):
        updates_in_order.append(update)
    else:
        updates_not_in_order.append(update)
part1(rules, updates_in_order)
part2(rules, updates_not_in_order)
