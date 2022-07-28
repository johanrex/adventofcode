import re
from dataclasses import dataclass


@dataclass
class PwdItem:
    rule_first: int
    rule_second: int
    rule_char: str
    pwd: str


with open("day2_input.txt") as f:
    lines = f.readlines()

pwd_items = []

# Example:
# 1-5 d: ndtdc
pat = re.compile(r"(\d+)-(\d+) ([a-z]): ([a-z]+)")

for line in lines:
    m = re.match(pat, line)
    item = PwdItem(
        rule_first=int(m.group(1)),
        rule_second=int(m.group(2)),
        rule_char=m.group(3),
        pwd=m.group(4),
    )
    pwd_items.append(item)
    pass


def part1():
    valid_count = 0

    item: PwdItem
    for item in pwd_items:
        if item.rule_first <= item.pwd.count(item.rule_char) <= item.rule_second:
            valid_count += 1

    print("Part 1:", valid_count)


def part2():
    valid_count = 0

    item: PwdItem
    for item in pwd_items:
        rule_char1 = item.pwd[item.rule_first - 1]
        rule_char2 = item.pwd[item.rule_second - 1]

        if rule_char1 != rule_char2 and (rule_char1 == item.rule_char or rule_char2 == item.rule_char):
            valid_count += 1

    print("Part 2:", valid_count)


part1()
part2()
