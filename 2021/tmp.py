#TODO explicit type aliases https://www.python.org/dev/peps/pep-0613/

from __future__ import annotations
from typing import List
from dataclasses import dataclass
import copy
import networkx as nx
import itertools

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

room_to_apod_mapper = {
    3: A,
    5: B,
    7: C,
    9: D
}

apod_to_room_mapper = {
    A: 3,
    B: 5,
    C: 7,
    D: 9
}


def create_graph() -> nx.Graph:
    G = nx.Graph()

    row = 1
    for col in range(1, 12):
        G.add_node( (row, col) )

        if col > 0:
            G.add_edge( (row, col), (row, col-1) )

    for row in range(2, 2 + ROOM_SLOTS):
        for col in [3,5,7,9]:
            G.add_node( (row, col) )
            G.add_edge( (row, col), (row-1, col) )

    return G


def get_start_state(lines):
    pos_apods = {}

    for row in range(2, 2 + ROOM_SLOTS):
        for col in [3,5,7,9]:
            pos_apods[(row, col)] = mapper[lines[row][col]]

    return pos_apods

def get_end_state(start_state):
    c = itertools.cycle([A, B, C, D])
    end_state = copy.deepcopy(start_state)
    
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

def is_free_path(G: nx.Graph, current_state: dict[tuple[int, int], int], src: tuple[int, int], dst: tuple[int, int]):

    paths = nx.shortest_simple_paths(G, src, dst)
    shortest_path = next(paths)

    found_other_apod_along_path = next(True for pos in shortest_path if pos in current_state, False)
    return not found_other_apod_along_path


def get_valid_room_pos(current_state: dict[tuple[int, int], int], current_pos: tuple[int, int]):

    assert is_hallway(current_pos)

    apod = current_state[current_pos]

    assert apod != 0

    dst_room_col = apod_to_room_mapper[apod]

    current_col = current_pos[1]

    assert current_col != dst_room_col

    room_coordinates = [(depth, dst_room_col) for depth in range(2, 2+ROOM_SLOTS)]

    is_other_apod_in_room = next(True for room_coordinate in room_coordinates if room_coordinate in current_state, False)

    if is_other_apod_in_room:
        return False

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

def get_valid_moves(pos, current_state):
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


def sort(G, current_state, end_state):
    for pos in current_state:
        apod = current_state[pos]
        moves = get_valid_moves(pos, current_state)


filename = '2021/23_input_example.txt'
lines = read_input(filename)

start_state = get_start_state(lines)
end_state = get_end_state(start_state)

G = create_graph()

is_free_path(G, start_state, (3,3), (1, 1) )

sort(G, start_state, end_state)
#get_reachable_vertices(G, start_state, (2, 3) )


import pickle
buf = pickle.dumps(None)
copy = pickle.loads(buf)

i = 0
