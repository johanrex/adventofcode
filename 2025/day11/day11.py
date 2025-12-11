from dataclasses import dataclass
import time
import math
import re
import copy
from collections import Counter
import sys
import os
from collections import defaultdict
import itertools

Graph = dict[set[str]]


def parse(filename: str) -> Graph:
    graph = defaultdict(set)
    with open(filename) as f:
        for line in f:
            line = line.strip()
            toks = [x.replace(":", "") for x in line.split(" ")]
            graph[toks[0]] = set(toks[1:])
    return graph


def part1(graph: Graph):
    def dfs(graph: Graph, start: str, goal: str, path: list[str]):
        path = path + [start]

        if start == goal:
            nonlocal total_paths
            total_paths.append(path)
            return

        for neighbor in graph[start]:
            if neighbor not in path:
                dfs(graph, neighbor, goal, path)

    total_paths = []
    dfs(graph, "you", "out", [])

    print("Part 1:", len(total_paths))


def part2(graph: Graph):
    def dfs(graph: Graph, start: str, goal: str, path: set[str]):
        path = path | {start}

        if start == goal:
            nonlocal dac_fft_paths
            if "dac" in path and "fft" in path:
                dac_fft_paths += 1
            return

        for neighbor in graph[start]:
            if neighbor not in path:
                dfs(graph, neighbor, goal, path)

    dac_fft_paths = 0
    dfs(graph, "svr", "out", set())

    print("Part 2:", dac_fft_paths)


filename = "day11/example"
filename = "day11/input"

graph = parse(filename)
part1(graph)
part2(graph)
