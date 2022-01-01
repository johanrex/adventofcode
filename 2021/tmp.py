#TODO explicit type aliases https://www.python.org/dev/peps/pep-0613/

from __future__ import annotations
from typing import List
from dataclasses import dataclass
import itertools
import functools

ROOM_SLOTS = 2

A = 1
B = 2
C = 3
D = 4

mapper = {
    'A' : A,
    'B' : B,
    'C' : C,
    'D' : D
}

apod_to_room_mapper = {
    A: 3,
    B: 5,
    C: 7,
    D: 9
}


def get_start_state(lines):
    pos_apods = {}

    for row in range(2, 2 + ROOM_SLOTS):
        for col in [3,5,7,9]:
            pos_apods[(row, col)] = mapper[lines[row][col]]

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

def get_valid_room_pos(current_state: dict[tuple[int, int], int], current_pos: tuple[int, int]):

    assert is_hallway(current_pos)

    apod = current_state[current_pos]

    assert apod != 0

    dst_room_col = apod_to_room_mapper[apod]

    current_col = current_pos[1]

    assert current_col != dst_room_col

    room_coordinates = [(depth, dst_room_col) for depth in range(2, 2+ROOM_SLOTS)]

    is_other_apod_in_room = next((True for room_coordinate in room_coordinates if room_coordinate in current_state), False)

    if is_other_apod_in_room:
        return None

    first_free_pos_from_bottom = next(reversed(room_coordinate for room_coordinate in room_coordinates if room_coordinate not in current_state), None)
    if first_free_pos_from_bottom is not None:
        return first_free_pos_from_bottom


def get_valid_hallway_positions(current_state: dict[tuple[int, int], int], start_pos: tuple[int, int]):

    assert not is_hallway(start_pos)

    positions = []

    #check if we can move out of room. 
    start_row = start_pos[0]
    start_col = start_pos[1]

    if start_row > 2:
        for row in range(start_row, 1, -1):
            if not is_free_pos(current_state, (row, start_col) ):
                return None


    leftmost_col = 1
    for col in range(start_col, leftmost_col-1, -1):
        pos = (1, col)
        if is_free_pos(current_state, pos):
            if not is_no_parking(pos):
                positions.append(pos)
        else:
            break


    rightmost_col = 11
    for col in range(start_col, rightmost_col+1):
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
        valid_room_pos = get_valid_room_pos(current_state, pos)
        if valid_room_pos is not None:
            moves.append(valid_room_pos)
    else:
        tmp = get_valid_hallway_positions(current_state, pos)
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

@functools.cache
def cost_of_move(apod, src_pos, dst_pos):
    global A, B, C, D

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


def organize(current_state, end_state):

    costs = []

    __organize(current_state, end_state, costs)

    return costs


def __organize(current_state, end_state, costs, cost = 0):

    for pos in current_state:
        apod = current_state[pos]
        moves = get_valid_moves(current_state, pos)
        for move in moves:

            cost += cost_of_move(apod, pos, move)

            new_state = get_new_state(current_state, pos, move)
            if new_state == end_state:
                costs.append(cost)
            else:
                __organize(new_state, end_state, costs, cost)


filename = '2021/23_input_example.txt'
lines = read_input(filename)

start_state = get_start_state(lines)
end_state = get_end_state(start_state)

costs = organize(start_state, end_state)

print('Part 1:', next(iter(sorted(costs))))

i = 0
