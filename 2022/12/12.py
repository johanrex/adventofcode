import networkx as nx
import sys

ELEVATION = "elevation"


def print_graph_elevation(G):
    print(nx.get_node_attributes(G, ELEVATION))


def get_height(height_str: str):
    assert type(height_str) == str
    return (ord(height_str)) - ord("a") + 1


def parse(filename: str):
    grid = []
    with open(filename) as f:
        while line := f.readline():
            line = line.strip()
            grid.append(line)

    w = len(grid[0])
    h = len(grid)

    G = nx.DiGraph()

    start_node = None
    end_node = None

    # Add nodes
    for y in range(h):
        for x in range(w):
            elevation_str = grid[y][x]

            if elevation_str == "S":
                elevation_str = "a"
                start_node = (x, y)
            elif elevation_str == "E":
                elevation_str = "z"
                end_node = (x, y)

            elevation = get_height(elevation_str)
            G.add_node((x, y), elevation=elevation)

    print("Added these elevations:")
    print_graph_elevation(G)

    # Add edges
    for y in range(h):
        for x in range(w):

            curr = (x, y)
            neighbors = []

            # left neighbor
            if x > 0:
                neighbors.append((x - 1, y))

            # right neighbor
            if x < w - 1:
                neighbors.append((x + 1, y))

            # up neighbor
            if y > 0:
                neighbors.append((x, y - 1))

            # down neighbor
            if y < h - 1:
                neighbors.append((x, y + 1))

            current_elevation = G.nodes[curr][ELEVATION]
            for neighbor in neighbors:
                neighbor_elevation = G.nodes[neighbor][ELEVATION]

                if (neighbor_elevation - current_elevation) <= 1:
                    G.add_edge(curr, neighbor)

    return G, start_node, end_node


filename = "12/example"
# filename = "12/input"

G, start_node, end_node = parse(filename)

iterator = nx.bfs_predecessors(G, end_node, depth_limit=None, sort_neighbors=None)

pass

path = nx.shortest_path(G, start_node, end_node)
print("Part1:", len(path) - 1)

lowest_nodes = {node: elevation for (node, elevation) in nx.get_node_attributes(G, ELEVATION).items() if elevation == 1}.keys()

shortest = sys.maxsize
for node in lowest_nodes:
    try:
        path = nx.shortest_path(G, node, end_node)
        l = len(path)
        if l < shortest:
            shortest = l
    except:
        pass
print("Part2:", shortest - 1)

# johan    5,039213
pass
