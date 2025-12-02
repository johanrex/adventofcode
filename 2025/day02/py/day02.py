def parse(filename) -> list[tuple[int, int]]:
    with open(filename) as f:
        content = f.read().strip()
        content = content.replace("\n", "")
        content = content.replace("\r", "")
    tmp = content.split(",")
    intervals = []
    for part in tmp:
        toks = part.split("-")
        intervals.append((int(toks[0]), int(toks[1])))

    return intervals


def is_repeated_twice(num) -> bool:
    if num < 10:
        return False

    num_s = str(num)
    if len(num_s) % 2 == 1:
        return False

    repeated = num_s[: len(num_s) // 2] * 2
    return repeated == num_s


def is_repeated_at_least_twice(num) -> bool:
    if num < 10:
        return False

    num_s = str(num)
    L = len(num_s)

    for i in range(L // 2):
        if L % (i + 1) != 0:
            continue

        part = num_s[: i + 1]
        repeated = part * (L // (i + 1))
        if repeated == num_s:
            return True

    return False


def part1(intervals):
    invalids = set()
    for interval in intervals:
        start, end = interval
        for i in range(start, end + 1):
            if is_repeated_twice(i):
                invalids.add(i)

        # print(interval, " -> ", invalids)

    ans = sum(invalids)

    print("Part 1:", ans)


def part2(intervals):
    invalids = set()
    for interval in intervals:
        start, end = interval
        for i in range(start, end + 1):
            if is_repeated_at_least_twice(i):
                invalids.add(i)

        # print(interval, " -> ", invalids)

    ans = sum(invalids)

    print("Part 2:", ans)


# filename = "day02/example"
filename = "day02/input"

intervals = parse(filename)

part1(intervals)
part2(intervals)
