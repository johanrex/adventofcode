import networkx as nx
import numpy as np

def coord_to_node_name(row, col):
    return f'{col}_{row}'

filename = '2021/15_input.txt'
#filename = '2021/15_input_example.txt'

lines = []
with open(filename, 'r') as f:
    for line in f:
        lines.append(list(map(int, list(line.strip()))))

def risk(lines):

    nr_of_cols = len(lines[0])
    nr_of_rows = len(lines)

    g = nx.DiGraph()

    #add edges
    for row in range(nr_of_rows):
        for col in range(nr_of_cols):
            u = coord_to_node_name(row, col)

            if col > 0: #left neighbor?
                n_row = row
                n_col = col-1

                v = coord_to_node_name(n_row, n_col)

                g.add_edge(u, v, weight=lines[n_row][n_col])
                g.add_edge(v, u, weight=lines[row][col])

            if col < nr_of_cols-2: #right neighbor?
                n_row = row
                n_col = col+1

                v = coord_to_node_name(n_row, n_col)

                g.add_edge(u, v, weight=lines[n_row][n_col])
                g.add_edge(v, u, weight=lines[row][col])

            if row > 0: #up neighbor?
                n_row = row-1
                n_col = col

                v = coord_to_node_name(n_row, n_col)

                g.add_edge(u, v, weight=lines[n_row][n_col])
                g.add_edge(v, u, weight=lines[row][col])

            if row < nr_of_rows - 2: #down neighbor
                n_row = row+1
                n_col = col

                v = coord_to_node_name(n_row, n_col)

                g.add_edge(u, v, weight=lines[n_row][n_col])
                g.add_edge(v, u, weight=lines[row][col])

    start = coord_to_node_name(0,0)
    end = coord_to_node_name(nr_of_cols-1, nr_of_rows-1)

    path = nx.dijkstra_path(g, start, end, weight='weight')

    risk = 0

    prev = None

    for node in path:
        if prev == None:
            prev = node
        else:
            data = g.get_edge_data(prev, node)
            risk += data['weight']
            prev = node
    return risk

def iterate_mtx(m):
    m1 = m+1
    m1[m1>9]=1
    return m1

def append_mtx(*mtxv, axis):
    tmp = None
    for i in range(len(mtxv)):
        if i == 0:
            tmp = mtxv[i]
            continue
        else:
            tmp = np.append(tmp, mtxv[i], axis)

    return tmp

def grid_times_five(lines):
    m = np.asarray(lines)

    big_rows = m.shape[0]*5

    """
    01234
    12345
    23456
    34567
    45678
    """

    iterations = []
    for i in range(9):
        if i == 0:
            iterations.append(m)
        else:
            iterations.append(iterate_mtx(iterations[i-1]))

    big = append_mtx(
            append_mtx(iterations[0], iterations[1], iterations[2], iterations[3], iterations[4], axis=1),
            append_mtx(iterations[1], iterations[2], iterations[3], iterations[4], iterations[5], axis=1),
            append_mtx(iterations[2], iterations[3], iterations[4], iterations[5], iterations[6], axis=1),
            append_mtx(iterations[3], iterations[4], iterations[5], iterations[6], iterations[7], axis=1),
            append_mtx(iterations[4], iterations[5], iterations[6], iterations[7], iterations[8], axis=1),
            axis=0)

    #convert back to list of list... I should have used a numpy 2d array from the start...
    big_lines = []
    for row in big:
        big_lines.append(list(row))

    return big_lines

print('Part 1 risk:', risk(lines))

big_lines = grid_times_five(lines)

print('Part 2 risk:', risk(big_lines))

i=0
