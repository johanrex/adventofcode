from __future__ import annotations
from typing import List
from dataclasses import dataclass
import copy
import networkx as nx
import itertools

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

def create_graph() -> nx.Graph:
    G = nx.Graph()

    row = 1
    for col in range(1, 12):
        G.add_node( (row, col) )

        if col > 0:
            G.add_edge( (row, col), (row, col-1) )

    for row in range(2, 4):
        for col in [3,5,7,9]:
            G.add_node( (row, col) )
            G.add_edge( (row, col), (row-1, col) )

    return G


def get_start_state(lines):
    pos_apods = {}

    for row in range(2, 4):
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

def is_node_occupied(state: dict, pos: tuple[int, int]) -> bool:
    return pos in state

def is_no_parking(pos: tuple[int, int]):
    return pos in [(1,3), (1, 5), (1,7), (1,9)]

def is_hallway(pos: tuple(int, int)) -> bool:
    return pos[0] == 1

def get_reachable_vertices(G: nx.Graph, state: dict[tuple[int, int], int], source: tuple[int, int] ):

    paths = list(nx.dfs_edges(G, source=source))

    for path in paths:
        print(path)

        #Prune paths according to:
        #is_no_parking()
        #is_node_occupied()
        # is allowed room
        # move from room to hallway. (don't get stuck moving up and down in room)


def organize(G):
    pass

filename = '2021/23_input_example.txt'
lines = read_input(filename)

start_state = get_start_state(lines)
end_state = get_end_state(start_state)


G = create_graph()
get_reachable_vertices(G, start_state, (2, 3) )


import pickle
buf = pickle.dumps(None)
copy = pickle.loads(buf)

i = 0
