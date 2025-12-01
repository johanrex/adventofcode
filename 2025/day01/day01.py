def parse(filename):
    with open(filename) as f:
        data = f.read().strip().split("\n")

    return data


def part1(data):
    curr = 50
    pwd = 0

    for rot in data:
        direction = rot[0]
        steps = int(rot[1:])

        if direction == "L":
            curr = curr - steps

        elif direction == "R":
            curr = curr + steps

        curr = curr % 100

        if curr == 0:
            pwd += 1

    print("Part 1:", pwd)


def part2(data):
    curr = 50
    pwd = 0

    for rot in data:
        direction = rot[0]
        steps = int(rot[1:])
        passing_zero_cnt = 0

        if direction == "L":
            steps = -steps

        if steps < 0 and abs(steps) > curr:
            passing_zero_cnt = (abs(curr + steps) // 100) + 1
        if steps > 0:
            passing_zero_cnt = abs(curr + steps) // 100

        curr = curr + steps

        curr = curr % 100

        if curr == 0:
            pwd += 1
            if passing_zero_cnt > 0:
                passing_zero_cnt -= 1

        pwd += passing_zero_cnt

        if passing_zero_cnt > 0:
            print(
                f"The dial is rotated {rot} to point at {curr}. during this rotation, it points at 0 {passing_zero_cnt}."
            )
        else:
            print(f"The dial is rotated {rot} to point at {curr}.")

    print("Part 2:", pwd)


filename = "day01/example"
# filename = "day01/input"

data = parse(filename)
part1(data)
part2(data)
