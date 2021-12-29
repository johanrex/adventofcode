from __future__ import annotations
from typing import List
from dataclasses import dataclass
import copy

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

@dataclass
class Amphipod:
    type: int    
    pos: tuple

    def __str__(self) -> str:
        return 

class Graph:
    def __init__(self) -> None:
        self.vertices = []

    def add_vertex(self, v):
        assert v.id is not None
        
        already_in_graph = False
        for existing_v in self.vertices:
            if v.id == existing_v.id:
                already_in_graph = True
                break 
        
        assert already_in_graph == False

        print('Adding vertex:', v)

        self.vertices.append(v)

    def get_vertex_by_id(self, id: object) -> Graph.Vertex:
        v = next(vertex for vertex in self.vertices if vertex.id == id)
        return v

    @staticmethod
    def add_bidirectional_edge(v1, v2):
        if v1.edges is None:
            v1.edges = []

        if v2.edges is None:
            v2.edges = []

        v1.edges.append(v2)
        v2.edges.append(v1)
        
    @dataclass
    class Vertex:
        id: object
        value: object = None
        edges: List[Graph.Vertex] = None


def create_graph(lines):
    G = Graph()

    row = 1
    for col in range(11):
        G.add_vertex(Graph.Vertex(id=(row, col)))

        if col > 0:
            Graph.add_bidirectional_edge(
                G.get_vertex_by_id( (row, col)), 
                G.get_vertex_by_id( (row, col-1)))         

    for row in range(2, 4):
        for col in [3,5,7,9]:
            G.add_vertex(Graph.Vertex(id=(row, col)))
            Graph.add_bidirectional_edge(
                G.get_vertex_by_id( (row, col)),
                G.get_vertex_by_id( (row-1, col)))

    return G


def get_initial_pos(lines):
    amphipods = []
    for row in range(2, 4):
        for col in [3,5,7,9]:
            amphipods.append(Amphipod(mapper[lines[row][col]], pos=(row, col)))

    return amphipods

def get_end_pos(lines):
    amphipods = copy.deepcopy(get_initial_pos(lines))
    amphipods[0].value = A
    amphipods[1].value = B
    amphipods[2].value = C
    amphipods[3].value = D
    amphipods[4].value = A
    amphipods[5].value = B
    amphipods[6].value = C
    amphipods[7].value = D

    return amphipods


def read_input(filename):
    lines = []
    with open(filename) as f:
        for line in f:
            lines.append(line.replace('\n', ''))

    return lines 

def is_vertex_occupied(amphipods: List[Amphipod], id) -> bool:
    return next((True for a in amphipods if a.pos == id), False) == True

def is_hallway(vertex) -> bool:
    if vertex.id[0] == 1:
        return True
    else:
        return False

def get_reachable_vertices(G: Graph, amphipods: List[Amphipod], apod: Amphipod, ) -> List[Graph.Vertex]:
    tmp = []

    v = Graph.get_vertex_by_id(apod.pos)
    for v_neighbor in v.edges:
        if not is_vertex_occupied(G, v_neighbor.id):
            pass


def organize(G):
    pass

filename = '2021/23_input_example.txt'
lines = read_input(filename)

G = create_graph(lines)
amphipods = [v.value for v in G.vertices if v.value is not None]

import pickle
buf = pickle.dumps(amphipods)
copy = pickle.loads(buf)

i = 0