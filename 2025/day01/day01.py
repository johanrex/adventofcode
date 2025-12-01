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
            steps *= -1

        curr = curr + steps

        curr = curr % 100

        if curr == 0:
            pwd += 1

    assert pwd == 1034
    print("Part 1:", pwd)


def part2(data):
    curr = 50
    pwd = 0

    for rot in data:
        direction = rot[0]
        steps = int(rot[1:])

        if direction == "L":
            steps *= -1

        passing_zero_cnt = 0

        if steps > 0:
            passing_zero_cnt = (curr + steps) // 100
        elif steps < 0:
            if (curr + steps) <= 0:
                if curr == 0:
                    passing_zero_cnt = abs(curr + steps) // 100
                else:
                    passing_zero_cnt = (abs(curr + steps) // 100) + 1
        else:
            raise ValueError("steps cannot be zero")

        curr = curr + steps
        curr = curr % 100

        pwd += passing_zero_cnt

        # if passing_zero_cnt > 0:
        #     print(
        #         f"The dial is rotated {rot} to point at {curr}. during this rotation, it points at 0 {passing_zero_cnt}."
        #     )
        # else:
        #     print(f"The dial is rotated {rot} to point at {curr}.")

    print("Last position:", curr)

    assert pwd == 6166
    print("Part 2:", pwd)


# filename = "day01/example"
filename = "day01/input"

data = parse(filename)
part1(data)
part2(data)
