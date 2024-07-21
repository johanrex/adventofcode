from collections import Counter


def parse_groups(lines: list[str]):
    groups = []
    group = None
    for line in lines:
        if len(line.strip()) == 0:
            group = None
            continue

        if group is None:
            group = []
            groups.append(group)

        group.append(line)
    return groups


def p1_sum_groups(groups):
    group_sum = 0
    for group in groups:
        tmp = []
        for line in group:
            tmp.extend([*line])

        group_sum += len(set(tmp))
    return group_sum


def p2_sum_groups(groups):

    s = 0

    for group in groups:
        nr_of_individuals = len(group)

        whole_group = "".join(group)
        c = Counter(whole_group)

        for item in c:
            item_count = c[item]
            if nr_of_individuals == item_count:
                s += 1

    return s


def main():
    with open("day6_input.txt", "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]

    groups = parse_groups(lines)

    s1 = p1_sum_groups(groups)
    assert s1 == 6662
    print("Part 1:", s1)

    # 11907 too high
    s2 = p2_sum_groups(groups)
    assert s2 == 3382
    print("Part 2:", s2)


if __name__ == "__main__":
    main()
