import math

# filename = "3/example"
filename = "3/input"

with open(filename) as file:
    lines = [line.strip() for line in file]


def get_prio(c: str) -> int:
    if c.islower():
        p = ord(c) - ord("a") + 1
    else:
        p = ord(c) - ord("A") + 27
    return p


def part1():
    prios = 0
    for line in lines:
        l = len(line)
        assert l % 2 == 0
        c1, c2 = line[: l // 2], line[l // 2 :]
        s1, s2 = set(c1), set(c2)
        common = s1 & s2
        assert len(common) == 1
        c = next(iter(common))
        prios += get_prio(c)

    assert prios == 7917
    print(prios)


def part2():
    prios = 0
    for i in range(0, len(lines), 3):
        l1 = lines[i]
        l2 = lines[i + 1]
        l3 = lines[i + 2]

        common = set(l1) & set(l2) & set(l3)
        assert len(common) == 1
        c = next(iter(common))
        prios += get_prio(c)

    assert prios == 2585
    print(prios)


part1()
part2()
