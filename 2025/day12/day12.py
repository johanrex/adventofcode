def solve(filename):
    with open(filename) as f:
        lines = f.read().strip().splitlines()

    yes_cnt = 0
    no_cnt = 0

    i = 0
    while i < len(lines):
        line = lines[i]

        # is shape definition
        if line[1] == ":":
            i += 5
        else:
            first, second = line.split(": ")
            cols, rows = map(int, first.split("x"))
            quantities = list(map(int, second.split(" ")))

            area_needed = sum([9 * q for q in quantities])
            area_present = cols * rows

            if area_present >= area_needed:
                yes_cnt += 1
            else:
                no_cnt += 1

            i += 1

    print(f"Yes: {yes_cnt}, No: {no_cnt}")
    print("Answer:", yes_cnt)


# filename = "day12/example"
filename = "day12/input"

solve(filename)
