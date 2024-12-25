from collections import defaultdict

Graph = defaultdict[str, set[str]]


def parse(filename: str) -> Graph:
    graph: Graph = defaultdict(set)
    with open(filename) as f:
        for line in f.readlines():
            a, b = line.strip().split("-")
            graph[a].add(b)
            graph[b].add(a)
    return graph


def part1(graph: Graph):
    sets = set()
    ts = [node_name for node_name in graph.keys() if node_name.startswith("t")]
    for a in ts:
        for b in graph[a]:
            if b == a:
                continue
            for c in graph[b]:
                if c == b:
                    continue

                if a in graph[c]:
                    sets.add(tuple(sorted([a, b, c])))
    ans = len(sets)
    print("Part 1:", ans)


filename = "day23/example"
filename = "day23/input"

graph = parse(filename)
part1(graph)
