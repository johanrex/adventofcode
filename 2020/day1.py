with open("day1_input.txt") as f:
    lines = f.readlines()

lines = [int(line) for line in lines]
length = len(lines)


def part1():
    found = False
    for i in range(length):
        if not found:
            for j in range(i + 1, length):
                if lines[i] + lines[j] == 2020:
                    print("Part1:", lines[i] * lines[j])
                    found = True
                    break
    print("Done")


def part2():
    found = False
    for i in range(length):
        if not found:
            for j in range(i + 1, length):
                if not found:
                    for k in range(j + 1, length):
                        if lines[i] + lines[j] + lines[k] == 2020:
                            print("Part2:", lines[i] * lines[j] * lines[k])
                            found = True
                            break
    print("Done")


part1()
part2()
