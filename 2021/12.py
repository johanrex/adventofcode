
#input = edge list.

#detect is small cyclic
import copy
import pprint
from collections import defaultdict

filename = '2021/12_input_example.txt'

class Graph(object):

    def __init__(self):
        self._graph = defaultdict(set)

    def add(self, node1, node2):

        self._graph[node1].add(node2)
        self._graph[node2].add(node1)

    # def is_connected(self, node1, node2):
    #     return node1 in self._graph and node2 in self._graph[node1]

    # def find_path(self, node1, node2, path=[]):
    #     """ Find any path between node1 and node2 (may not be shortest) """

    #     path = path + [node1]
    #     if node1 == node2:
    #         return path
    #     if node1 not in self._graph:
    #         return None
    #     for node in self._graph[node1]:
    #         if node not in path:
    #             new_path = self.find_path(node, node2, path)
    #             if new_path:
    #                 return new_path
    #     return None

    def find_all_paths(self, node1, node2, path = []):
        paths=[]
        path=[]

        self.__find_all_paths(node1, node2, path, paths)

        return paths        

    def __find_all_paths(self, node1, node2, path, paths):

        path = path + [node1]
        if node1 == node2:
            paths.append(copy.deepcopy(path))
            return path
        if node1 not in self._graph:
            return None
        for node in self._graph[node1]:
            if node.islower() and node not in path:
                self.__find_all_paths(node, node2, path, paths)
            elif node.isupper() and node != path[len(path)-1]:

                self.__find_all_paths(node, node2, path, paths)

        return None        

    # def __str__(self):
    #     return '{}({})'.format(self.__class__.__name__, dict(self._graph))

g = Graph()

#read input
with(open(filename, "r")) as f:
    lines = [ line.strip().split('-') for line in f.readlines() ]
for line in lines:
    g.add(line[0], line[1])

pretty_print = pprint.PrettyPrinter()
pretty_print.pprint(g._graph)

lst = g.find_all_paths('start', 'end')
for path in lst:
    p = ','.join(path)
    print(p)

print('Part 1. Nr of paths:', len(lst))
i = 0