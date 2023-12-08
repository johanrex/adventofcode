import re
import networkx as nx
import sympy
import math


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


def get_next_move_generator(moves):
    while True:
        for move in moves:
            yield move


def all_ends_with_z(lst):
    for x in lst:
        if not x.endswith("Z"):
            return False
    return True


def get_steps(start, edge_lookup, move_gen):
    curr = start
    steps = 0
    while not curr.endswith("Z"):
        next_move = next(move_gen)

        key = curr + next_move

        step_to = edge_lookup[key]
        curr = step_to

        steps += 1

    return steps


def part2(moves, G):
    edge_lookup = {}
    edges = G.edges(data=True)

    # create edge lookup
    for u, v, data in G.edges(data=True):
        pass
        edge_name = data.get("label")
        edge_lookup[edge_name] = v

    curr_nodes = [node_name for node_name in list(G.nodes()) if node_name.endswith("A")]

    steps_list = []
    for curr in curr_nodes:
        # Start new generator for each starting node
        move_gen = get_next_move_generator(moves)

        steps = get_steps(curr, edge_lookup, move_gen)
        steps_list.append(steps)

    common_primes = set()

    for steps in steps_list:
        primes = sympy.primefactors(steps)
        print(f"{steps} has prime factors {primes}")

        common_primes.update(primes)

    print("all primes", common_primes)
    print("prod", math.prod(common_primes))


# filename = "8/example_p2"
filename = "8/input"

moves, G = parse(filename)
part2(moves, G)
