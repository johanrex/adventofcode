import json
import copy


def cmp(a, b) -> int:

    if type(a) == int and type(b) == int:
        if a < b:
            return -1
        elif a > b:
            return 1
        else:
            return 0

    elif type(a) == list and type(b) == list:
        l = max(len(a), len(b))
        for i in range(l):
            if i >= len(b):
                return 1
            elif i >= len(a):
                return -1
            else:
                res = cmp(a[i], b[i])
                if res != 0:
                    return res

    elif type(a) == int and type(b) == list:
        return cmp([a], b)
    elif type(a) == list and type(b) == int:
        return cmp(a, [b])
    else:
        raise Exception("nope")

    return 0


def flatten(lst: list) -> list:
    new = []
    for item in lst:
        if type(item) == list:
            new.extend(flatten(item))
        else:
            new.append(item)
    return new


def listify(old: list[int], idx):
    assert type(old[idx]) == int
    new = copy.deepcopy(old)
    new[idx] = [new[idx]]
    return new


# filename = "13/example"
filename = "13/input"
with open(filename) as f:
    lines = [line.strip() for line in f.readlines()]


correct_pair_idx = []
pair_idx = 1

for i in range(0, len(lines), 3):
    a = lines[i]
    b = lines[i + 1]

    # print(a)
    # print(b)

    a = json.loads(a)
    b = json.loads(b)

    result = cmp(a, b)
    print(result < 0)

    if result < 0:
        correct_pair_idx.append(pair_idx)

    pair_idx += 1

part1 = sum(correct_pair_idx)
assert part1 == 6046
print("Part1:", part1)

# -----------------------------------


lines.append("[[2]]")
lines.append("[[6]]")
lists = [json.loads(line) for line in lines if line != ""]


sorted_lists = sorted(lists, key=cmp_to_key(cmp))
