def solve(filename):
    with open(filename) as f:
        lines = f.read().strip().splitlines()

    certain_fit = 0
    uncertain_fit = 0

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

            region_area = cols * rows
            area_needed = sum([9 * q for q in quantities])

            if region_area >= area_needed:
                certain_fit += 1
            else:
                uncertain_fit += 1

            i += 1

    print(f"Certain fit: {certain_fit}, Uncertain fit: {uncertain_fit}")
    print("Answer:", certain_fit)


# filename = "day12/example"
filename = "day12/input"

solve(filename)
