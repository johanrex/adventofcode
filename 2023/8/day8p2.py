import re
import networkx as nx


def parse(filename):
    with open(filename) as f:
        line = f.readline().strip()
        moves = [c for c in line]

        # G = nx.Graph()
        G = nx.MultiDiGraph()

        line = f.readline().strip()
        assert line == ""

        for line in f:
            line = line.strip()
            if line == "":
                break
            match = re.match(r"(\w+)\s*=\s*\((\w+),\s*(\w+)\)", line)
            node_name = match.group(1)
            left = match.group(2)
            right = match.group(3)

            if not G.has_node(node_name):
                G.add_node(node_name, name=node_name)
            if not G.has_node(left):
                G.add_node(left, name=left)
            if not G.has_node(right):
                G.add_node(right, name=right)

            G.add_edge(node_name, left, label=f"{node_name}L")
            G.add_edge(node_name, right, label=f"{node_name}R")
            pass

    return moves, G


def get_next_move(moves):
    while True:
        for move in moves:
            yield move


def all_ends_with_z(lst):
    for x in lst:
        if not x.endswith("Z"):
            return False
    return True


def part2(moves, G):
    edge_lookup = {}
    edges = G.edges(data=True)

    for u, v, data in G.edges(data=True):
        pass
        edge_name = data.get("label")
        edge_lookup[edge_name] = v

    curr_nodes = [node_name for node_name in list(G.nodes()) if node_name.endswith("A")]

    move_gen = get_next_move(moves)
    steps = 0
    print("starting part 2")

    while not all_ends_with_z(curr_nodes):
        next_move = next(move_gen)

        keys = [curr + next_move for curr in curr_nodes]
        step_tos = [edge_lookup[key] for key in keys]

        curr_nodes = step_tos
        steps += 1

    print("Part 2:", steps)


# filename = "8/example_p2"
filename = "8/input"

moves, G = parse(filename)
part2(moves, G)
