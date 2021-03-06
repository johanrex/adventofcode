import itertools
from timeit import default_timer as timer

# 3.8 compatible type hints for pypy. Silly capital letters. Better in 3.10.
from typing import Tuple, Dict, List

PositionType = Tuple[int, int]
StateType = Dict[PositionType, int]


positions_evaluated = None
states_processed_memo = None
lowest_end_state_cost = None

ROOM_LEVELS = None

A = 1
B = 2
C = 3
D = 4

char_to_int_mapper = {"A": A, "B": B, "C": C, "D": D}
int_to_char_mapper = {A: "A", B: "B", C: "C", D: "D"}

apod_to_room_mapper = {A: 3, B: 5, C: 7, D: 9}
room_to_apod_mapper = {3: A, 5: B, 7: C, 9: D}

start_timer = timer()


def init_global_variables():
    global positions_evaluated
    global states_processed_memo
    global lowest_end_state_cost

    positions_evaluated = 0
    states_processed_memo = {}
    lowest_end_state_cost = 10000000


def hash_state(current_state: StateType, cost: int) -> int:
    keys = sorted(current_state.keys())
    lst = [(key, current_state[key]) for key in keys]
    lst.append(cost)
    return hash(tuple(lst))


def get_start_state(lines) -> StateType:
    pos_apods = {}

    for row in range(2, 2 + ROOM_LEVELS):
        for col in [3, 5, 7, 9]:
            pos_apods[(row, col)] = char_to_int_mapper[lines[row][col]]

    return pos_apods


def get_end_state(start_state: StateType) -> StateType:

    end_state = start_state.copy()

    c = itertools.cycle([A, B, C, D])

    for key in end_state.keys():
        end_state[key] = next(c)

    return end_state


def read_input(filename, is_part_1):
    global ROOM_LEVELS

    lines = []
    with open(filename) as f:
        for line in f:
            lines.append(line.replace("\n", ""))

    if is_part_1:
        ROOM_LEVELS = 2
    else:
        lines.insert(3, "  #D#C#B#A#")
        lines.insert(4, "  #D#B#A#C#")

        ROOM_LEVELS = 4

    return lines


def is_free_pos(state: dict, pos: PositionType) -> bool:
    return pos not in state


def is_no_parking(pos: PositionType) -> bool:
    return pos in [(1, 3), (1, 5), (1, 7), (1, 9)]


def is_hallway(pos: PositionType) -> bool:
    return pos[0] == 1


def get_dst_pos_in_room(current_state: StateType, dst_room_col) -> PositionType:

    for row in range(1 + ROOM_LEVELS, 2 - 1, -1):

        pos = (row, dst_room_col)

        if pos not in current_state:
            return pos
        else:
            if current_state[pos] != room_to_apod_mapper[dst_room_col]:
                return None

    return None


def move_from_hallway_to_room(
    current_state: StateType, current_pos: PositionType
) -> PositionType:

    assert is_hallway(current_pos)

    apod = current_state[current_pos]

    dst_room_col = apod_to_room_mapper[apod]

    src_col = current_pos[1]

    assert src_col != dst_room_col

    dst_room_pos = get_dst_pos_in_room(current_state, dst_room_col)

    if dst_room_pos is None:
        return None
    else:

        if src_col < dst_room_col:
            r = range(src_col + 1, dst_room_col)
        else:
            r = range(src_col - 1, dst_room_col, -1)

        for col in r:
            if (1, col) in current_state:
                return None  # hallway blocked

        return dst_room_pos


def should_move_out_of_room(current_state: StateType, start_pos: PositionType) -> bool:

    assert not is_hallway(start_pos)

    apod = current_state[start_pos]

    src_room = start_pos[1]
    dst_room = apod_to_room_mapper[apod]

    correct_room = src_room == dst_room
    is_free_above = True
    is_wrong_apod_under = False

    for room_level in range(2, 2 + ROOM_LEVELS):
        if room_level < start_pos[0]:
            above = (room_level, src_room)
            if above in current_state:
                is_free_above = False

        if room_level > start_pos[0]:
            below = (room_level, src_room)
            if below in current_state and current_state[below] != apod:
                is_wrong_apod_under = True

    if correct_room:
        if is_wrong_apod_under and is_free_above:
            return True
        else:
            return False
    else:
        if is_free_above:
            return True
        else:
            return False


def move_from_room_to_hallway(
    current_state: StateType, src_pos: PositionType
) -> PositionType:

    assert not is_hallway(src_pos)

    # check if we should move out of room.
    if not should_move_out_of_room(current_state, src_pos):
        return None

    positions = []

    start_col = src_pos[1]

    leftmost_col = 1
    for col in range(start_col - 1, leftmost_col - 1, -1):
        pos = (1, col)
        if is_free_pos(current_state, pos):
            if not is_no_parking(pos):
                positions.append(pos)
        else:
            break

    rightmost_col = 11
    for col in range(start_col + 1, rightmost_col + 1):
        pos = (1, col)
        if is_free_pos(current_state, pos):
            if not is_no_parking(pos):
                positions.append(pos)
        else:
            break

    return positions


def get_moves(current_state: StateType, pos: PositionType) -> List[PositionType]:
    moves = []

    if is_hallway(pos):
        valid_room_pos = move_from_hallway_to_room(current_state, pos)
        if valid_room_pos is not None:
            moves.append(valid_room_pos)
    else:
        tmp = move_from_room_to_hallway(current_state, pos)
        if tmp is not None:
            moves.extend(tmp)

    return moves


def get_new_state(
    old_state: StateType, src_pos: PositionType, dst_pos: PositionType
) -> StateType:

    new_state = old_state.copy()

    assert src_pos != dst_pos
    assert dst_pos not in new_state

    new_state[dst_pos] = new_state[src_pos]
    del new_state[src_pos]

    return new_state


def cost_of_move(apod, src_pos: PositionType, dst_pos: PositionType) -> int:
    global A, B, C, D

    assert src_pos != dst_pos

    if apod == A:
        multiple = 1
    elif apod == B:
        multiple = 10
    elif apod == C:
        multiple = 100
    elif apod == D:
        multiple = 1000
    else:
        raise Exception("no")

    steps = abs(src_pos[0] - dst_pos[0]) + abs(src_pos[1] - dst_pos[1])

    return steps * multiple


def organize(
    current_state: StateType,
    end_state: StateType,
    cost: int = 0,
):

    hash = hash_state(current_state, cost)

    if hash in states_processed_memo:
        return
    else:
        states_processed_memo[hash] = 1

    global lowest_end_state_cost
    global positions_evaluated

    for src_pos, apod in current_state.items():

        dst_positions = get_moves(current_state, src_pos)

        for dst_pos in dst_positions:

            new_cost = cost + cost_of_move(apod, src_pos, dst_pos)

            if new_cost > lowest_end_state_cost:
                continue

            new_state = get_new_state(current_state, src_pos, dst_pos)

            if new_state == end_state:

                if new_cost < lowest_end_state_cost:
                    print("New lowest cost:", new_cost)
                    lowest_end_state_cost = new_cost
            else:
                organize(new_state, end_state, new_cost)

        positions_evaluated += len(dst_positions)


def print_burrow(current_state: StateType):

    lines = []
    lines.append(list("#############"))
    lines.append(list("#...........#"))
    lines.append(list("###.#.#.#.###"))
    for _ in range(ROOM_LEVELS - 1):
        lines.append(list("  #.#.#.#.#  "))

    lines.append(list("  #########  "))

    for pos, apod in current_state.items():
        lines[pos[0]][pos[1]] = int_to_char_mapper[apod]

    for lst in lines:
        print("".join(lst))


def solve(filename, is_part_1):
    global start_timer

    init_global_variables()

    lines = read_input(filename, is_part_1)

    start_state = get_start_state(lines)
    end_state = get_end_state(start_state)

    organize(start_state, end_state)

    print(
        f"Lowest end state cost: {lowest_end_state_cost}. Positions evaluated: {positions_evaluated}. Time elapsed: {timer() - start_timer}."
    )


# filename = '2021/23_input_example.txt'
filename = "2021/23_input.txt"

print("Part 1")
solve(filename, True)  # 14148

print("")

print("Part 2")
solve(filename, False)  # 43814
