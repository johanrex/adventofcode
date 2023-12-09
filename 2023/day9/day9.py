def parse(filename):
    histories = []
    with open(filename) as f:
        for line in f:
            strs = line.strip().split()
            nrs = [int(s) for s in strs]
            histories.append(nrs)

    return histories


def is_all_zero(nrs):
    for nr in nrs:
        if nr != 0:
            return False
    return True


def difference(nrs):
    diff = [0] * (len(nrs) - 1)
    for i in range(len(nrs) - 1):
        diff[i] = nrs[i + 1] - nrs[i]
    return diff


def extrapolate(history, last=True):
    sequences = []
    sequences.append(history)

    diff = history
    while not is_all_zero(diff):
        diff = difference(diff)
        sequences.append(diff)

    new_val = 0
    for seq in reversed(sequences):
        if last:
            val = seq[-1]
            new_val += val
        else:
            val = seq[0]
            new_val = val - new_val
        pass

    return new_val


def part1(histories):
    s = 0
    for history in histories:
        nr = extrapolate(history)
        s += nr

    assert s == 1974913025
    print("Part 1:", s)


def part2(histories):
    s = 0
    for history in histories:
        nr = extrapolate(history, last=False)
        s += nr

    assert 884 == s
    print("Part 2:", s)


# filename = "day9/example"
filename = "day9/input"

histories = parse(filename)
part1(histories)
part2(histories)
