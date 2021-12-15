from queue import PriorityQueue
# import numpy as np
# import networkx as nx
# import matplotlib.pyplot as plt

class Graph:
    def __init__(self, num_of_vertices):
        self.v = num_of_vertices
        self.edges = [[-1 for i in range(num_of_vertices)] for j in range(num_of_vertices)]
        self.visited = []

    def add_edge(self, u, v, weight):
        self.edges[u][v] = weight
        self.edges[v][u] = weight        

def dijkstra(graph, start_vertex):
    D = {v:float('inf') for v in range(graph.v)}
    D[start_vertex] = 0

    pq = PriorityQueue()
    pq.put((0, start_vertex))

    while not pq.empty():
        (dist, current_vertex) = pq.get()
        graph.visited.append(current_vertex)

        for neighbor in range(graph.v):
            if graph.edges[current_vertex][neighbor] != -1:
                distance = graph.edges[current_vertex][neighbor]
                if neighbor not in graph.visited:
                    old_cost = D[neighbor]
                    new_cost = D[current_vertex] + distance
                    if new_cost < old_cost:
                        pq.put((new_cost, neighbor))
                        D[neighbor] = new_cost
    return D

# g = Graph(9)
# g.add_edge(0, 1, 4)
# g.add_edge(0, 6, 7)
# g.add_edge(1, 6, 11)
# g.add_edge(1, 7, 20)
# g.add_edge(1, 2, 9)
# g.add_edge(2, 3, 6)
# g.add_edge(2, 4, 2)
# g.add_edge(3, 4, 10)
# g.add_edge(3, 5, 5)
# g.add_edge(4, 5, 15)
# g.add_edge(4, 7, 1)
# g.add_edge(4, 8, 5)
# g.add_edge(5, 8, 12)
# g.add_edge(6, 7, 1)
# g.add_edge(7, 8, 3) 

# D = dijkstra(g, 0)

# print(D)

# for vertex in range(len(D)):
#     print("Distance from vertex 0 to vertex", vertex, "is", D[vertex])

filename = '2021/15_input.txt'
lines = []
with open(filename, 'r') as f:
    for line in f:
        lines.append(list(map(int, list(line.strip()))))

g = Graph(len(lines)*len(lines[0]))

nr_of_cols = len(lines[0])
nr_of_rows = len(lines)

for row in range(nr_of_rows):
    for col in range(nr_of_cols):
        u = row*nr_of_cols + col

        if col > 0: #left neighbor?
            v = u-1
            g.add_edge(u, v, lines[row][col-1])
            g.add_edge(v, u, lines[row][col])
        if col < nr_of_cols-2: #right neighbor?
            neighbor = f'{row}_{col+1}'
            v = u+1
            g.add_edge(u, v, lines[row][col+1])
            g.add_edge(v, u, lines[row][col])
        if row > 0: #up neighbor?
            v = u - nr_of_cols
            g.add_edge(u, v, lines[row-1][col])
            g.add_edge(v, u, lines[row][col])
        if row < nr_of_rows - 2: #down neighbor
            v = u + nr_of_cols
            g.add_edge(u, v, lines[row+1][col])
            g.add_edge(v, u, lines[row][col])

D = dijkstra(g, 0)

# for vertex in range(len(D)):
#     print("Distance from vertex 0 to vertex", vertex, "is", D[vertex])


print('Part 1 risk:', D[(nr_of_rows*nr_of_cols)-1])

i = 0