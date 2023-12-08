import sympy
import math


def parse(filename):
    with open(filename) as f:
        line = f.readline().strip()
        moves = [c for c in line]

        node_names = []
        move_lookup = {}

        line = f.readline().strip()
        assert line == ""

        for line in f:
            line = line.strip()

            if line == "":
                break

            node_name = line[0:3]
            left = line[7:10]
            right = line[12:15]

            node_names.append(node_name)

            move_lookup[f"{node_name}L"] = left
            move_lookup[f"{node_name}R"] = right

    return moves, node_names, move_lookup


def get_next_move_generator(moves):
    while True:
        for move in moves:
            yield move


def all_ends_with_z(lst):
    for x in lst:
        if not x.endswith("Z"):
            return False
    return True


def dbg_inspect_cycles(start, move_lookup):
    curr = start

    print("Inspecting cycles starting with", start)

    move_gen = get_next_move_generator(moves)
    init_new_cycle = True
    steps = 0
    cycle_counter = 0
    while cycle_counter < 5:
        if init_new_cycle:
            print("cycle starts with:", curr)
            steps = 0
            init_new_cycle = False

        next_move = next(move_gen)
        key = curr + next_move
        curr = move_lookup[key]

        steps += 1

        if curr.endswith("Z"):
            print(f"cycle ends with: {curr}. Steps: {steps}")
            init_new_cycle = True
            cycle_counter += 1


def get_steps(curr, move_lookup, move_gen):
    steps = 0
    while not curr.endswith("Z"):
        next_move = next(move_gen)

        key = curr + next_move

        step_to = move_lookup[key]
        curr = step_to

        steps += 1

    return steps


def part2(moves, node_names, move_lookup):
    curr_nodes = [node_name for node_name in node_names if node_name.endswith("A")]

    for curr in curr_nodes:
        dbg_inspect_cycles(curr, move_lookup)

    steps_list = []
    for curr in curr_nodes:
        # Start new generator for each starting node
        move_gen = get_next_move_generator(moves)

        steps = get_steps(curr, move_lookup, move_gen)
        steps_list.append(steps)

    common_primes = set()

    for steps in steps_list:
        primes = sympy.primefactors(steps)
        print(f"{steps} has prime factors {primes}")

        common_primes.update(primes)

    print("all primes", common_primes)
    print("prod", math.prod(common_primes))

    print("...")

    print("Steps list", steps_list)
    print("lcm", math.lcm(*steps_list))


# filename = "8/example_p2"
filename = "8/input"

moves, node_names, move_lookup = parse(filename)
part2(moves, node_names, move_lookup)
