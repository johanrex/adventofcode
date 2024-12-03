import re

re_instr = re.compile(r"mul\(\d+,\d+\)|do\(\)|don't\(\)")
re_mul = re.compile(r"mul\(\d+,\d+\)")


def get_all_text(filename: str):
    with open(filename) as f:
        text = f.read()

    return text


def get_operands(mul: str):
    mul = mul[4:-1]
    a, b = mul.split(",")
    return int(a), int(b)


def part1(filename: str):
    text = get_all_text(filename)
    muls = re_mul.findall(text)

    s = 0
    for mul in muls:
        a, b = get_operands(mul)
        s += a * b

    assert s == 161289189
    print("Part 1:", s)


def part2(filename):
    text = get_all_text(filename)
    instructions = re_instr.findall(text)

    s = 0
    do = True
    for instr in instructions:
        if instr.startswith("don't"):
            do = False
        elif instr.startswith("do"):
            do = True
        elif instr.startswith("mul"):
            if do:
                a, b = get_operands(instr)
                s += a * b

    assert s == 83595109
    print("Part 2:", s)


# filename = "day3/example"
filename = "day3/input"

part1(filename)
part2(filename)
