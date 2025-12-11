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

Graph = dict[list[str]]


def parse(filename: str) -> Graph:
    graph = defaultdict(list)
    with open(filename) as f:
        for line in f:
            line = line.strip()
            toks = [x.replace(":", "") for x in line.split(" ")]
            graph[toks[0]] = toks[1:]
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
    dfs(graph, "svr", "out", [])

    ans = 0

    for path in total_paths:
        found_dac = False
        found_fft = False
        for node in path:
            if node == "dac":
                found_dac = True
            if node == "fft":
                found_fft = True

        if found_dac and found_fft:
            ans += 1

    print("Part 2:", ans)


filename = "day11/example"
filename = "day11/input"

graph = parse(filename)
part1(graph)
part2(graph)
