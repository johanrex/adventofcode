#filename = "10/example"
filename = "10/input"


def parse(filename):
    curr_cycle = 1
    x_reg = 1
    cycle_x = {}

    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line == "noop":
                cycle_x[curr_cycle] = x_reg
                curr_cycle += 1
            else:
                instr, val = line.split()
                if instr == "addx":
                    cycle_x[curr_cycle] = x_reg
                    cycle_x[curr_cycle + 1] = x_reg

                    x_reg += int(val)
                    curr_cycle += 2
                else:
                    raise ValueError(f"Unknown instruction {instr}")

    return cycle_x


def part1(mapper):
    sum_of_signal_strengths = 0
    cycles_to_check = [x for x in range(20, 220 + 1, 40)]

    for c in cycles_to_check:
        sum_of_signal_strengths += c * mapper[c]

    return sum_of_signal_strengths


def part2(mapper):
    crt_width = 40
    crt_height = 6

    crt = ["."] * (crt_width * crt_height)

    def print_crt(crt):
        start = 0
        end = crt_width

        while end <= len(crt):
            print("".join(crt[start:end]))
            start += crt_width
            end += crt_width

    for cycle in range(1, len(crt) + 1):
        x_val = mapper[cycle]
        cycle_mod = cycle % crt_width
        if x_val <= cycle_mod <= x_val + 2:
            crt[cycle - 1] = "#"

    print_crt(crt)


cycle_x_mapper = parse(filename)
print("Part1:", part1(cycle_x_mapper))
part2(cycle_x_mapper)
