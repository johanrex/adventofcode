# 128 rows
# 8 columns


def bsp(boardingpass):

    row_min = 0
    row_max = 127

    col_min = 0
    col_max = 7

    for instr in boardingpass[0:7]:
        if instr == "F":
            row_max = row_max - ((row_max + 1 - row_min) // 2)
        elif instr == "B":
            row_min = row_min + ((row_max + 1 - row_min) // 2)

    for instr in boardingpass[7:10]:
        if instr == "L":
            col_max = col_max - ((col_max + 1 - col_min) // 2)
        elif instr == "R":
            col_min = col_min + ((col_max + 1 - col_min) // 2)

    assert col_min == col_max
    assert row_min == row_max

    return row_min, col_min


def coord_to_id(row, col) -> int:
    return row * 8 + col


if __name__ == "__main__":
    with open("day5_input.txt") as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    ids = [coord_to_id(*bsp(line)) for line in lines]

    print("Part 1:", max(ids))

    ids = sorted(ids)

    for i in range(len(ids) - 1):
        a = ids[i]
        b = ids[i + 1]

        if (b - a) == 2:
            print(f"Part 2. {a} and {b} is in list. Thus {a+1} is my id.")
