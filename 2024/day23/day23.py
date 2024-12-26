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


def get_cliques(graph: Graph) -> set[tuple[str]]:
    def bron_kerbosch(r: set[str], p: set[str], x: set[str]):
        if not p and not x:
            cliques.add(tuple(sorted(r)))
        for v in list(p):
            r_v = r | {v}
            p_v = p & graph[v]
            x_v = x & graph[v]
            bron_kerbosch(r_v, p_v, x_v)
            p.remove(v)
            x.add(v)

    cliques = set()
    bron_kerbosch(set(), set(graph.keys()), set())
    return cliques


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


def part2(graph: Graph):
    cliques = get_cliques(graph)
    cs_list = list(cliques)
    cs_list.sort(key=lambda x: len(x), reverse=True)
    max_clique = cs_list[0]
    ans = ",".join(max_clique)

    assert ans == "bg,bu,ce,ga,hw,jw,nf,nt,ox,tj,uu,vk,wp"

    print("Part 2:", ans)


filename = "day23/example"
filename = "day23/input"

graph = parse(filename)
part1(graph)
part2(graph)
