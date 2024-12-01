from collections import Counter


def parse(filename):
    lst1 = []
    lst2 = []

    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            toks = line.split()
            a = int(toks[0])
            b = int(toks[1])

            lst1.append(a)
            lst2.append(b)

    lst1.sort()
    lst2.sort()

    return lst1, lst2


def part1(lst1, lst2):
    diffs = [abs(lst2[i] - lst1[i]) for i in range(len(lst1))]
    s = sum(diffs)

    assert s == 1110981
    print("Part 1:", s)


def part2(lst1, lst2):
    c = Counter(lst2)

    s = 0

    for n in lst1:
        prod = n * c[n]
        s += prod

    assert s == 24869388
    print("Part 2:", s)


# filename = "day1/example"
filename = "day1/input"

lst1, lst2 = parse(filename)
part1(lst1, lst2)
part2(lst1, lst2)
