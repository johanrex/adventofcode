from collections import defaultdict
import re
import networkx as nx

PAT = re.compile(r"Valve (.*) has flow rate=(\d+); tunnel(s)? lead(s)? to valve(s)? (.*)")
FLOW_RATE = "flow_rate"
OPEN = "open"


def parse_line(line: str) -> tuple[str, int, list[str]]:
    m = re.match(PAT, line)

    if m is None:
        raise Exception("oops")

    valve_id = m.group(1)
    flow_rate = int(m.group(2))
    to_valves = m.group(6).split(", ")

    return (valve_id, flow_rate, to_valves)


def parse_input(filename):
    data = []
    with open(filename) as f:
        lines = f.readlines()
        data = [parse_line(line.strip()) for line in lines]
    return data


def print_graph(G):
    print("This is the graph:")
    for node in G.nodes:
        print(node, list(G.neighbors(node)))
    print("-----------------")


def build_graph(data):
    G = nx.Graph()

    for item in data:
        valve_id = item[0]
        flow_rate = item[1]
        G.add_node(valve_id, flow_rate=flow_rate, open=False)

    for item in data:
        valve_id = item[0]
        to_valves = item[2]

        for to_valve in to_valves:
            G.add_edge(valve_id, to_valve)

    return G


def node_selection_heuristic(node):
    return node[FLOW_RATE]


# Function that implements the bfs algorithm
def bfs(graph, source_node):

    time = -1
    pressure = 0

    # Initialize the queue with the source node
    queue = [source_node]
    # Initialize the visited nodes set
    visited = set()
    # Initialize the path list
    path = []
    # While the queue is not empty
    while queue:
        # Get the first node in the queue
        node = queue.pop(0)
        # Add the node to the visited nodes set
        visited.add(node)
        # Add the node to the path
        path.append(node)

        # Move
        time += 1

        print("")
        print(f"== Minute {time} ==")
        print(f"Valves {[id for id, attrs in graph.nodes(data=True) if attrs[OPEN] == True]} are open, releasing {pressure} pressure.")
        print(f"You move to valve {node}.")

        # print(f"Moved to node {node}. Current time: {time}. Pressure: {pressure}")

        # Open valve
        if graph.nodes[node][FLOW_RATE] > 0 and not graph.nodes[node][OPEN]:
            time += 1
            print("")
            print(f"== Minute {time} ==")
            print(f"Valves {[id for id, attrs in graph.nodes(data=True) if attrs[OPEN] == True]} are open, releasing {pressure} pressure.")
            print(f"You open valve {node}.")

            graph.nodes[node][OPEN] = True

        # Add pressure from all open valves
        pressure += sum([(attrs[FLOW_RATE]) for id, attrs in graph.nodes(data=True) if attrs[OPEN] == True])

        # Get the neighbors of the node
        neighbors = graph.neighbors(node)
        # For each neighbor
        for neighbor in neighbors:
            # If the neighbor is not in the visited nodes set
            if neighbor not in visited:
                # Add the neighbor to the queue
                queue.append(neighbor)

    # Print the path
    print("Pressure:", pressure)
    print("Path:", path)


if __name__ == "__main__":
    filename = "16/example"
    # filename = "16/input"
    data = parse_input(filename)

    G = build_graph(data)
    print_graph(G)

    bfs(G, "AA")
    pass

    # for source_node in G.nodes:

    #     # nx.maximum_flow(G,source_node, sink_node, capacity="flow_rate", )
    #     # path = nx.bfs_beam_edges(G, sink_node, node_selection_heuristic, width=2)
    #     beam_search(G, source_node)

    #     pass
