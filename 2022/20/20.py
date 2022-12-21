import sys


# använd en curkulär linked list istället kanske. Med referenser till objekt i en annan lista som håller ursprungliga ordningen.


def __mix(data: list[int], idx_from) -> tuple[list[int], list[int]]:
    new = data.copy()
    new_idxs = list(range(len(data)))

    item = data[idx_from]

    if (idx_from + item) <= 0:  # do we have negative wrap around?
        idx_to = (idx_from + item) % len(data) - 1
    else:  # positive
        idx_to = ((idx_from + item) + len(data)) % len(data)

    if idx_to > idx_from:
        for i in range(len(data)):
            if i < idx_from:
                continue
            elif idx_from <= i < idx_to:
                new[i] = data[i + 1]
                new_idxs[i + 1] = i
            elif i == idx_to:
                new[i] = item
                new_idxs[idx_from] = idx_to

    return new, new_idxs


filename = "20/example"
with open(filename) as f:
    data = [int(line.strip()) for line in f.readlines()]

print("Initial arrangement:")
print(data)


# example i=0
assert __mix([1, 2, -3, 3, -2, 0, 4], 0)[0] == [2, 1, -3, 3, -2, 0, 4]

# example i=1
assert __mix([2, 1, -3, 3, -2, 0, 4], 0)[0] == [1, -3, 2, 3, -2, 0, 4]

# example i=2
assert __mix([1, -3, 2, 3, -2, 0, 4], 1)[0] == [1, 2, 3, -2, -3, 0, 4]

# example i=3
assert __mix([1, 2, 3, -2, -3, 0, 4], 2)[0] == [1, 2, -2, -3, 0, 3, 4]

# example i=4
assert __mix([1, 2, -2, -3, 0, 3, 4], 2)[0] == [1, 2, -3, 0, 3, 4, -2]


pass

# nope
assert __mix([4, -2, 5, 6, 7, 8, 9], 1)[0] == [4, 5, 6, 7, 8, -2, 9]

# ok
assert __mix([4, 15, 5, 6, 7, 8, 9], 1)[0] == [4, 5, 15, 6, 7, 8, 9]
assert __mix([4, 14, 5, 6, 7, 8, 9], 1)[0] == [4, 14, 5, 6, 7, 8, 9]
assert __mix([4, 7, 5, 6, 7, 8, 9], 1)[0] == [4, 7, 5, 6, 7, 8, 9]

# ok
assert __mix([4, -15, 5, 6, 7, 8, 9], 1)[0] == [-15, 4, 5, 6, 7, 8, 9]
assert __mix([4, -14, 5, 6, 7, 8, 9], 1)[0] == [4, -14, 5, 6, 7, 8, 9]
assert __mix([4, -7, 5, 6, 7, 8, 9], 1)[0] == [4, -7, 5, 6, 7, 8, 9]

assert __mix([4, -1, 5, 6, 7, 8, 9], 1)[0] == [-1, 4, 5, 6, 7, 8, 9]
assert __mix([4, 5, 6, 1, 7, 8, 9], 3)[0] == [4, 5, 6, 7, 1, 8, 9]


# assert mix([1, 2, -3, 3, -2, 0, 4]) == [2, 1, -3, 3, -2, 0, 4]
# assert mix([4, 5, 6, 1, 7, 8, 9]) == [4, 5, 6, 7, 1, 8, 9]
