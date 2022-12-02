def parse():
    lst = []
    grp = None
    with open("1/input") as f:
        for line in f:
            line = line.strip()

            if len(line) == 0:
                lst.append(grp)
                grp = None
                continue

            if grp == None:
                grp = []

            grp.append(int(line))
        lst.append(grp)
    return lst


def part1():
    max_sum = 0

    for grp in lst:
        s = sum(grp)
        if s > max_sum:
            max_sum = s

    # assert max_sum == 74394
    print("Max elf:", max_sum)


def part2():
    sums = []

    for grp in lst:
        s = sum(grp)
        sums.append(s)

    sums.sort(reverse=True)

    print("Top 3 elf cals:", sums[0] + sums[1] + sums[2])


lst = parse()
part1()
part2()
