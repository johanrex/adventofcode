import re

re_instr = re.compile(r"mul\(\d+,\d+\)|do\(\)|don't\(\)")
re_mul = re.compile(r"mul\((\d+),(\d+)\)")


def get_all_text(filename: str):
    with open(filename) as f:
        line = f.read()

    return line


def part1(filename: str):
    text = get_all_text(filename)
    muls = re_mul.findall(text)

    s = 0
    for mul in muls:
        a = int(mul[0])
        b = int(mul[1])
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
                m = re_mul.match(instr)
                a = int(m.group(1))
                b = int(m.group(2))

                s += a * b

    assert s == 83595109
    print("Part 2:", s)


# filename = "day3/example"
filename = "day3/input"

part1(filename)
part2(filename)
