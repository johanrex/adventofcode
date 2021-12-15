import networkx as nx

def coord_to_node_name(row, col):
    return f'{col}_{row}'

#filename = '2021/15_input.txt'
filename = '2021/15_input_example.txt'
lines = []
with open(filename, 'r') as f:
    for line in f:
        lines.append(list(map(int, list(line.strip()))))

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

print('Part 1 risk:', risk)
i=0
