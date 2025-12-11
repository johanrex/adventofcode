from collections import defaultdict

Graph = dict[set[str]]


def parse(filename: str) -> Graph:
    graph = defaultdict(set)
    with open(filename) as f:
        for line in f:
            line = line.strip()
            toks = [x.replace(":", "") for x in line.split(" ")]
            graph[toks[0]] = set(toks[1:])
    return graph


def dfs(graph: Graph, curr: str, target: str, memo: dict[str:int]) -> int:
    if curr == target:
        return 1

    if curr in memo:
        return memo[curr]

    neighbor_paths = 0
    for neighbor in graph[curr]:
        neighbor_paths += dfs(graph, neighbor, target, memo)

    memo[curr] = neighbor_paths
    return neighbor_paths


def part1(graph: Graph):
    nr_paths = dfs(graph, "you", "out", {})
    print("Part 1:", nr_paths)


def part2(graph: Graph):
    a = dfs(graph, "svr", "fft", {})
    b = dfs(graph, "fft", "dac", {})
    c = dfs(graph, "dac", "out", {})
    nr_paths = a * b * c
    print("Part 2:", nr_paths)


filename = "day11/example"
filename = "day11/input"

graph = parse(filename)
part1(graph)
part2(graph)
