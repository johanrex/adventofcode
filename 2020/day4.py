from collections import defaultdict
from dataclasses import dataclass
import re

mandatory_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}

re_hgt = re.compile(r"(\d+)(cm|in)")
re_hcl = re.compile(r"#(\d|[a-f]){6}")
re_ecl = re.compile(r"amb|blu|brn|gry|grn|hzl|oth")
re_pid = re.compile(r"\d{9}")


def part1_valid(d: dict) -> bool:
    if len(mandatory_fields - set(d.keys())) == 0:
        return True
    else:
        return False


def part2_valid(d: dict) -> bool:

    d = defaultdict(str) | d

    if len(set(d.keys()) - mandatory_fields - {"cid"}) != 0:
        return False

    val = d["byr"]
    if not (len(val) == 4 and 1920 <= int(val) <= 2002):
        return False

    val = d["iyr"]
    if not (len(val) == 4 and 2010 <= int(val) <= 2020):
        return False

    val = d["eyr"]
    if not (len(val) == 4 and 2020 <= int(val) <= 2030):
        return False

    val = d["hgt"]
    hgt_valid = False
    if (m := re.match(re_hgt, val)) and len(m.groups()) == 2 and m.group(1).isnumeric():
        cm_valid = "cm" == m.group(2) and 150 <= int(m.group(1)) <= 193
        in_valid = "in" == m.group(2) and 59 <= int(m.group(1)) <= 76
        if cm_valid or in_valid:
            hgt_valid = True

    if not hgt_valid:
        return False

    val = d["hcl"]
    if not re.match(re_hcl, val):
        return False

    val = d["ecl"]
    if not re.match(re_ecl, val):
        return False

    val = d["pid"]
    if not re.match(re_pid, val):
        return False

    return True


def record_to_dict(record) -> dict:
    kvps = []
    for line in record:
        kvps.extend(line.split())

    d = {}
    for kvp in kvps:
        key, value = kvp.split(":", 1)
        d[key] = value

    return d


def parse_passports(lines, validator_func):
    valid_count = 0
    current_record = None

    for line in lines:
        if line == "":
            d = record_to_dict(current_record)
            if validator_func(d):
                valid_count += 1
            current_record = None
            continue

        if current_record is None:
            current_record = []

        current_record.append(line)

    return valid_count


if __name__ == "__main__":
    with open("day4_input.txt") as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    print("Part1:", parse_passports(lines, part1_valid))
    print("Part2:", parse_passports(lines, part2_valid))
