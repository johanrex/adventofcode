def find_marker(s: str) -> int:
    ret = -1
    for i in range(4, len(s)):
        chunk = s[i - 4 : i]
        if len(set(chunk)) == 4:
            ret = i
            break
    return ret


def find_message(s: str) -> int:
    ret = -1
    for i in range(14, len(s)):
        chunk = s[i - 14 : i]
        if len(set(chunk)) == 14:
            ret = i
            break
    return ret


assert find_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 7
assert find_message("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 19

with open("6/input") as f:
    s = f.read()

print("Part1:", find_marker(s))  # 1658
print("Part2:", find_message(s))  # 2260
