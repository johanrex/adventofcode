from collections import Counter


def parse(filename):
    res = []
    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            toks = line.split()
            a = int(toks[0])
            b = int(toks[1])
            res.append((a, b))
    return res


def part1(data):
    lst1 = [item[0] for item in data]
    lst2 = [item[1] for item in data]

    lst1.sort()
    lst2.sort()

    diffs = [abs(lst2[i] - lst1[i]) for i in range(len(lst1))]
    s = sum(diffs)

    assert s == 1110981
    print("Part 1:", s)


def part2(data):
    lst1 = [item[0] for item in data]
    lst2 = [item[1] for item in data]

    c = Counter(lst2)

    s = 0

    for n in lst1:
        prod = n * c[n]
        s += prod

    assert s == 24869388
    print("Part 2:", s)


# filename = "day1/example"
filename = "day1/input"

data = parse(filename)
part1(data)
part2(data)
