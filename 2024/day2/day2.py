import re
import copy


def parse_ints(filename: str):
    nrs = []
    with open(filename) as f:
        for line in f:
            nrs.append(list(map(int, re.findall(r"\d+", line))))
    return nrs


def is_safe(line):
    diffs = [a - b for a, b in zip(line, line[1:])]

    same_sign = all(d > 0 for d in diffs) or all(d < 0 for d in diffs)
    nice_diff = all(1 <= abs(d) <= 3 for d in diffs)

    safe = same_sign and nice_diff
    return safe


def part1(data):
    safe_cnt = 0
    for line in data:
        if is_safe(line):
            safe_cnt += 1

    assert safe_cnt == 479
    print("Part 1:", safe_cnt)


def part2(data):
    safe_cnt = 0
    for line in data:
        if is_safe(line):
            safe_cnt += 1
        else:
            for k in range(len(line)):
                line_copy = copy.deepcopy(line)

                line_copy.pop(k)

                if is_safe(line_copy):
                    safe_cnt += 1
                    break

    assert safe_cnt == 531
    print("Part 2:", safe_cnt)


# filename = "day2/example"
filename = "day2/input"

data = parse_ints(filename)
part1(data)
part2(data)
