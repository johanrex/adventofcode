def find_unique(s: str, substr_length: int) -> int:
    ret = -1
    for i in range(substr_length, len(s)):
        chunk = s[i - substr_length : i]
        if len(set(chunk)) == substr_length:
            ret = i
            break
    return ret


# assert find_unique("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 4) == 7
# assert find_unique("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14) == 19

with open("6/input") as f:
    s = f.read()

print("Part1:", find_unique(s, 4))  # 1658
print("Part2:", find_unique(s, 14))  # 2260
