#TODO explicit type aliases https://www.python.org/dev/peps/pep-0613/

from __future__ import annotations
import pickle
from typing import List
from dataclasses import dataclass
import itertools
import functools
from timeit import default_timer as timer

positions_evaluated = 0

ROOM_LEVELS = 2

A = 1
B = 2
C = 3
D = 4

char_to_int_mapper = {'A':A,'B':B,'C':C,'D':D}
int_to_char_mapper = {A:'A',B:'B',C:'C',D:'D'}

apod_to_room_mapper = {
    A: 3,
    B: 5,
    C: 7,
    D: 9
}


def get_start_state(lines):
    pos_apods = {}

    for row in range(2, 2 + ROOM_LEVELS):
        for col in [3,5,7,9]:
            pos_apods[(row, col)] = char_to_int_mapper[lines[row][col]]

    return pos_apods

def get_end_state(start_state):

    end_state = start_state.copy()

    c = itertools.cycle([A, B, C, D])
    
    for key in end_state.keys():
        end_state[key] = next(c)
    
    return end_state


def read_input(filename):
    lines = []
    with open(filename) as f:
        for line in f:
            lines.append(line.replace('\n', ''))

    return lines 

def is_free_pos(state: dict, pos: tuple[int, int]) -> bool:
    return pos not in state

def is_no_parking(pos: tuple[int, int]):
    return pos in [(1,3), (1, 5), (1,7), (1,9)]

def is_hallway(pos: tuple(int, int)) -> bool:
    return pos[0] == 1

def move_from_hallway_to_room(current_state: dict[tuple[int, int], int], current_pos: tuple[int, int]):

    #print_burrow(current_state)

    assert is_hallway(current_pos)

    apod = current_state[current_pos]

    assert apod != 0

    dst_room_col = apod_to_room_mapper[apod]

    current_col = current_pos[1]

    assert current_col != dst_room_col

    hallway_from_col = min(current_col, dst_room_col)
    hallway_to_col = max(current_col, dst_room_col)

    #TODO kanske göra en funktion som kollar om en lista med positions är blockerade. 
    hallway_positions = ( (1, col) for col in range(hallway_from_col+1, hallway_to_col+1) )
    is_hallway_blocked = next( (True for pos in hallway_positions if pos in current_state), False)

    if is_hallway_blocked:
        return None

    dst_room_positions = [(depth, dst_room_col) for depth in range(2, 2+ROOM_LEVELS)]

    is_other_apod_in_room = next((True for dst_room_pos in dst_room_positions if dst_room_pos in current_state and current_state[dst_room_pos] != apod), False)

    # print_burrow(current_state)
    # print(current_pos)

    if is_other_apod_in_room:
        return None
    else:
        first_free_pos_from_bottom = next((dst_room_pos for dst_room_pos in reversed(dst_room_positions) if dst_room_pos not in current_state), None)
        if first_free_pos_from_bottom is not None:
            return first_free_pos_from_bottom

    return None

def should_move_out_of_room(current_state: dict[tuple[int, int], int], start_pos: tuple[int, int]):

    assert not is_hallway(start_pos)

    apod = current_state[start_pos]

    src_room = start_pos[1]
    dst_room = apod_to_room_mapper[apod]

    correct_room = src_room == dst_room
    is_free_above = True
    is_wrong_apod_under = False

    for room_level in range(2, 2+ROOM_LEVELS):
        if room_level < start_pos[0]:
            above = (room_level, src_room)
            if above in current_state and current_state[above] != apod:
                is_free_above = False
        
        if room_level > start_pos[0]:
            below = (room_level, src_room)
            if below in current_state and current_state[below] != apod:
                is_wrong_apod_under = True

    ##TODO detta kommer inte funka om room är mer än 2 djup...
    if not correct_room and is_free_above:
        return True
    elif is_wrong_apod_under:
        return True
    else:
        return False

def move_from_room_to_hallway(current_state: dict[tuple[int, int], int], start_pos: tuple[int, int]):

    assert not is_hallway(start_pos)

    # print_burrow(current_state)
    # print(start_pos)

    # check if we should move out of room. 
    if not should_move_out_of_room(current_state, start_pos):
        return None

    positions = []

    start_col = start_pos[1]

    leftmost_col = 1
    for col in range(start_col-1, leftmost_col-1, -1):
        pos = (1, col)
        if is_free_pos(current_state, pos):
            if not is_no_parking(pos):
                positions.append(pos)
        else:
            break


    rightmost_col = 11
    for col in range(start_col+1, rightmost_col+1):
        pos = (1, col)
        if is_free_pos(current_state, pos):
            if not is_no_parking(pos):
                positions.append(pos)
        else:
            break

    return positions

def get_valid_moves(current_state, pos):
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

def get_new_state(old_state, src_pos, dst_pos):

    new_state = old_state.copy()

    assert src_pos != dst_pos
    assert dst_pos not in new_state

    new_state[dst_pos] = new_state[src_pos]
    del new_state[src_pos]

    return new_state

#@functools.cache
def cost_of_move(apod, src_pos, dst_pos):
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
        raise Exception('no')

    steps = abs(src_pos[0] - dst_pos[0]) + abs(src_pos[1] - dst_pos[1])

    return steps * multiple


def serialize_state(state):
    return pickle.dumps(state)

states_processed = {}
lowest_total_cost = 10000000
lowest_total_cost_moves = []
def organize(current_state, end_state, cost:int = 0, total_path = []):

    current_state_serialized = serialize_state(current_state)
    
    if current_state_serialized in states_processed:
        return
    else:
        states_processed[current_state_serialized] = 1

    global lowest_total_cost
    global lowest_total_cost_moves
    global positions_evaluated

    for src_pos, apod in current_state.items():

        dst_positions = get_valid_moves(current_state, src_pos)

        # print('')
        # print('In this state:')
        # print_burrow(current_state)
        # print(f'Found {len(moves)} moves for apod at {pos}.')

        for dst_pos in dst_positions:
            
            new_total_path = total_path.copy()
            new_total_path.append( (src_pos, dst_pos) )

            new_cost = cost + cost_of_move(apod, src_pos, dst_pos)

            if new_cost > lowest_total_cost:
                continue

            new_state = get_new_state(current_state, src_pos, dst_pos)
            
            if new_state == end_state: 
                
                if new_cost < lowest_total_cost:
                    print('New lowest cost:', new_cost)
                    lowest_total_cost = new_cost

                    lowest_total_cost_moves = new_total_path

                    time_elapsed = timer() - start_timer
                    print(f'Evaluating {positions_evaluated/time_elapsed} positions/s.')
            else:
                organize(new_state, end_state, new_cost, new_total_path)

        positions_evaluated += 1


def print_burrow(current_state):

    lines = []
    lines.append(list('#############'))
    lines.append(list('#...........#'))
    lines.append(list('###.#.#.#.###'))
    for _ in range(ROOM_LEVELS-1):
        lines.append(list('  #.#.#.#.#  '))

    lines.append(list('  #########  '))

    for pos, apod in current_state.items():
        lines[pos[0]][pos[1]] = int_to_char_mapper[apod]

    for lst in lines:
        print(''.join(lst))



start_timer = timer()

filename = '2021/23_input_example.txt'
#filename = '2021/23_input.txt'
lines = read_input(filename)


start_state = get_start_state(lines)
end_state = get_end_state(start_state)

organize(start_state, end_state)

print('Positions evaluated:', positions_evaluated)

print('Part 1:', lowest_total_cost)

for move in lowest_total_cost_moves:
    print(move)


i = 0
