from dataclasses import dataclass


@dataclass
class State:
    cycle_nr: int
    reg_x_val: int


def op_noop(current_state: State) -> State:
    return State(current_state.cycle_nr + 1, current_state.reg_x_val)


def op_addx(current_state: State, value: int) -> State:
    return State(current_state.cycle_nr + 2, current_state.reg_x_val + value)


filename = "10/input"

part1_sum_of_signal_strengths = 0
cycles_to_check = [x for x in range(20, 220 + 1, 40)]

current_state = State(0, 1)
with open(filename) as f:
    for line in f:
        if len(cycles_to_check) == 0:
            break

        line = line.strip()
        old_state = current_state
        if line == "noop":
            current_state = op_noop(old_state)
        elif line.startswith("addx"):
            instr, val = line.split()
            current_state = op_addx(old_state, int(val))

        cycle = cycles_to_check[0]

        val = None
        if old_state.cycle_nr <= cycle <= current_state.cycle_nr:
            val = old_state.reg_x_val

        if val is not None:
            signal_strength = cycle * val
            part1_sum_of_signal_strengths += signal_strength
            cycles_to_check.pop(0)
            print(signal_strength)
            # print(part1_sum_of_signal_strengths)

print("Part1:", part1_sum_of_signal_strengths)


def print(crt):

    for line in crt:
        print("".join(line))


crt = [["."] * 40] * 6
