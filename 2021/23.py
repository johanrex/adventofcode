from __future__ import annotations
from typing import List
from dataclasses import dataclass

Initial_state = \
"""
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""

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

    def get_vertex_by_id(self, id: object):
        v = next(vertex for vertex in self.vertices if vertex.id == id)
        return v

    @staticmethod
    def add_bidirectional_edge(v1, v2):
        if v1.edges is None:
            v1.edges = []

        if v2.edges is None:
            v2.edges = []

        v1.edges.append(Graph.Edge(destination=v2))
        v2.edges.append(Graph.Edge(destination=v1))
        
    @dataclass
    class Vertex:
        id: object
        value: int
        edges: List[Graph.Edge] = None

    @dataclass
    class Edge:
        destination: Graph.Vertex

def create_graph(lines):
    G = Graph()

    row = 1
    for col in range(11):
        G.add_vertex(Graph.Vertex(id=(row, col), value=None))

        if col > 0:
            Graph.add_bidirectional_edge(
                G.get_vertex_by_id( (row, col)), 
                G.get_vertex_by_id( (row, col-1)))         

    for row in range(2, 4):
        for col in [3,5,7,9]:
            apod = Amphipod(mapper[lines[row][col]], pos=(row, col))
            G.add_vertex(Graph.Vertex(id=(row, col), value=apod))
            Graph.add_bidirectional_edge(
                G.get_vertex_by_id( (row, col)),
                G.get_vertex_by_id( (row-1, col)))

    return G

def read_input(filename):
    lines = []
    with open(filename) as f:
        for line in f:
            lines.append(line.replace('\n', ''))

    return lines 

def get_valid_moves():
    pass

def organize(G):
    pass

filename = '2021/23_input_example.txt'
lines = read_input(filename)

G = create_graph(lines)
amphipods = [v.value for v in G.vertices if v.value is not None]

i = 0

