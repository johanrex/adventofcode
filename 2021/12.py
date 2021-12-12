import copy
import pprint
from collections import defaultdict
from timeit import default_timer as timer
t1 = timer()

class Graph(object):

    def __init__(self):
        self._graph = defaultdict(set)

    def add(self, node1, node2):

        self._graph[node1].add(node2)
        self._graph[node2].add(node1)

    def find_all_paths(self, traverse_option, node1, node2, path = []):
        paths=[]
        path=[]

        self.__find_all_paths(traverse_option, node1, node2, path, paths)

        return paths        

    def __find_all_paths(self, traverse_option, node1, node2, path, paths):

        path = path + [node1]
        if node1 == node2:
            paths.append(copy.deepcopy(path))
            return path
        if node1 not in self._graph:
            return None
        for node in self._graph[node1]:

            if traverse_option == 1:
                if node.islower() and node not in path:
                    self.__find_all_paths(traverse_option, node, node2, path, paths)
                elif node.isupper() and node != path[len(path)-1]:
                    self.__find_all_paths(traverse_option, node, node2, path, paths)
            else:
                if node.islower() and node != 'start':

                    if node not in path:
                        self.__find_all_paths(traverse_option, node, node2, path, paths)
                    else:
                        #count, groupby lower
                        any_more_than_1 = False
                        any_more_than_1 = any(True for x in path if x.islower() and path.count(x) > 1)

                        if not any_more_than_1:
                            self.__find_all_paths(traverse_option, node, node2, path, paths)

                elif node.isupper() and node != path[len(path)-1]:
                    self.__find_all_paths(traverse_option, node, node2, path, paths)

        return None        

g = Graph()

filename = '2021/12_input.txt'

#read input
with(open(filename, "r")) as f:
    lines = [ line.strip().split('-') for line in f.readlines() ]
for line in lines:
    g.add(line[0], line[1])

pretty_print = pprint.PrettyPrinter()
pretty_print.pprint(g._graph)

lst = g.find_all_paths(1, 'start', 'end')
print('Part 1. Nr of paths:', len(lst))

lst = g.find_all_paths(2, 'start', 'end')
print('Part 2. Nr of paths:', len(lst))

t2 = timer()
print(f'time: {(t2-t1):.4f}s')
