import re

re_instr = re.compile(r"mul\(\d+,\d+\)|do\(\)|don't\(\)")


def get_operands(mul: str):
    mul = mul[4:-1]
    a, b = mul.split(",")
    return int(a), int(b)


# filename = "day3/example"
filename = "day3/input"

with open(filename) as f:
    instructions = re_instr.findall(f.read())

s1 = 0
s2 = 0
do = True
for instr in instructions:
    if instr.startswith("mul"):
        a, b = get_operands(instr)
        s1 += a * b
        if do:
            s2 += a * b
    elif instr.startswith("don't"):
        do = False
    elif instr.startswith("do"):
        do = True

assert s1 == 161289189
print("Part 1:", s1)

assert s2 == 83595109
print("Part 2:", s2)
