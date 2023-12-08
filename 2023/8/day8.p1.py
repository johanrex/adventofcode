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

            move_lookup[f"{node_name}L"] = left
            move_lookup[f"{node_name}R"] = right

    return moves, move_lookup


def get_next_move(moves):
    while True:
        for move in moves:
            yield move


def part1(moves, move_lookup):
    start = "AAA"

    move_gen = get_next_move(moves)
    curr = start
    steps = 0

    while curr != "ZZZ":
        next_move = next(move_gen)

        key = curr + next_move
        step_to = move_lookup[key]

        curr = step_to
        steps += 1

    print("Part 1:", steps)


# filename = "8/example"
filename = "8/input"

moves, move_lookup = parse(filename)
part1(moves, move_lookup)
