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
    pattern = r"(?=(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty))"

    number_map = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "eleven": 11,
        "twelve": 12,
        "thirteen": 13,
        "fourteen": 14,
        "fifteen": 15,
        "sixteen": 16,
        "seventeen": 17,
        "eighteen": 18,
        "nineteen": 19,
        "twenty": 20,
    }

    s = 0
    for line in data:
        matches = list(re.finditer(pattern, line, re.IGNORECASE))
        if len(matches) > 0:
            first = matches[0].group(1)
            first = str(first)
            if first in number_map:
                first = str(number_map[first])

            last = matches[-1].group(1)
            last = str(last)
            if last in number_map:
                last = str(number_map[last])

            first = first[0]
            last = last[-1]

            line_number = int(first + last)
            s += line_number

            print(line, " -> ", line_number)
        else:
            assert False

    print("Part2", s)

    pass


# filename = "1/example_p2"
filename = "1/input"
with open(filename) as f:
    data = [line.strip() for line in f.readlines()]

# part1(data)


# wrong 53355
part2(data)
