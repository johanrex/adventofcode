import re

re_mul = re.compile(r"mul\((\d+),(\d+)\)")
re_do = re.compile(r"do\(\)")
re_dont = re.compile(r"don't\(\)")


def part1(filename: str):
    with open(filename) as f:
        lines = f.readlines()

    s = 0
    for line in lines:
        muls = re_mul.findall(line)

        for mul in muls:
            a = int(mul[0])
            b = int(mul[1])
            s += a * b

    assert s == 161289189
    print("Part 1:", s)


def get_all_matches(line, regex):
    matches = []
    for match in regex.finditer(line):
        matches.append((match.start(), match.group()))
    return matches


def part2(filename):
    with open(filename) as f:
        lines = f.readlines()

    line = "".join(lines)

    instr_list = []
    instr_list.extend(get_all_matches(line, re_mul))
    instr_list.extend(get_all_matches(line, re_do))
    instr_list.extend(get_all_matches(line, re_dont))

    # sort by position of match
    instr_list.sort(key=lambda x: x[0])

    mul_list = []
    do = True
    for instr in instr_list:
        if instr[1].startswith("don't"):
            do = False
        elif instr[1].startswith("do"):
            do = True
        elif instr[1].startswith("mul"):
            if do:
                mul_list.append(instr[1])

    s = 0
    for mul in mul_list:
        m = re_mul.match(mul)
        a = int(m.group(1))
        b = int(m.group(2))

        s += a * b

    assert s == 83595109
    print("Part 2:", s)


# filename = "day3/example"
filename = "day3/input"

part1(filename)
part2(filename)
