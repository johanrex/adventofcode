import re


def part1(data):
    s = 0
    for line in data:
        matches = re.findall(r"\d+", line)
        assert matches
        first = matches[0]
        if len(first) > 1:
            first = first[0]
        last = matches[-1]
        if len(last) > 1:
            last = last[-1]
        s += int(first + last)

    # assert s == 54644

    print("Part1", s)


def part2(data):
    words = "one two three four five six seven eight nine".split()
    number_map = {word: str(i) for i, word in enumerate(words, 1)}
    pattern = "(?=(\d+|" + "|".join(words) + "))"

    s = 0
    for line in data:
        matches = list(re.finditer(pattern, line, re.IGNORECASE))
        if len(matches) > 0:
            first = str(matches[0].group(1))
            last = str(matches[-1].group(1))

            if first in number_map:
                first = str(number_map[first])

            if last in number_map:
                last = str(number_map[last])

            first = first[0]
            last = last[-1]

            line_number = int(first + last)
            s += line_number
        else:
            assert False

    assert 53348 == s
    print("Part2", s)

    pass


# filename = "1/example_p2"
filename = "1/input"
with open(filename) as f:
    data = [line.strip() for line in f.readlines()]

part1(data)


# Bloody edge cases:
# 512ninexrqpvktwoner
# mfourjcxsvss3oneightlxh
# 188btpjkpdsix3oneightkpl
# eight26vhjjz4foureightwojk
# vgchkqhxrbjnlqnvpml77twonejcv

part2(data)
