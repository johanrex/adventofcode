def parse(filename: str) -> list:
    with open(filename, "r") as file:
        lines = file.readlines()

    instructions = []
    for line in lines:
        instr, val = line.strip().split(" ")
        instructions.append((instr, int(val)))

    return instructions


def execute(instructions: list) -> tuple[int, bool]:
    instructions_count = [0] * len(instructions)
    acc = 0
    current_instr_idx = 0
    infinite_loop = False
    while True:
        if current_instr_idx == len(instructions):
            infinite_loop = False
            break

        if instructions_count[current_instr_idx] == 1:
            infinite_loop = True
            break

        instr, arg = instructions[current_instr_idx]
        instructions_count[current_instr_idx] += 1

        if instr == "acc":
            acc += arg
            current_instr_idx += 1
        elif instr == "jmp":
            current_instr_idx += arg
        elif instr == "nop":
            current_instr_idx += 1
        else:
            raise ValueError("Invalid instruction")

    return acc, infinite_loop


filename = "day8/input"
instructions = parse(filename)

acc, _ = execute(instructions)
print("Part1:", str(acc))

for i in range(len(instructions)):
    instr, val = instructions[i]
    if instr == "jmp":
        instr = "nop"
    elif instr == "nop":
        instr = "jmp"
    else:
        continue

    mutated = instructions.copy()
    mutated[i] = (instr, val)

    acc, infinite_loop = execute(mutated)
    if not infinite_loop:
        print("Part2:", str(acc))
        break
