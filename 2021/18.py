
from collections import deque
import re
r = re.compile(r'\d+')

parse_line_idx = None

class Pair:
    def __init__(self) -> None:
        self.left = None
        self.right = None
        self.parent = None

    def __str__(self):
        if type(self.left) == Pair:
            str_left = str(self.left)
        else:
            str_left = self.left

        if type(self.right) == Pair:
            str_right = str(self.right)
        else:
            str_right = self.right

        s = f'[{str_left},{str_right}]'

        return s


def parse_line(s):
    global parse_line_idx
    parse_line_idx = 0 
    p = __parse_pair(s)
    return p


def __parse_element(s, parent):
    global parse_line_idx
    e = None

    if s[parse_line_idx] == '[':
        #is pair
        e = __parse_pair(s, parent)
    else:
        #is number
        m = r.match(s[parse_line_idx:])

        if not bool(m):
            raise Exception('expected number')

        e = int(m[0])

        parse_line_idx += len(m[0])
    
    return e


def __parse_pair(s, parent = None):
    global parse_line_idx

    assert s[parse_line_idx] == '['

    p = Pair()
    if parent != None:
        p.parent = parent

    #skip opening [
    parse_line_idx += 1

    p.left = __parse_element(s, p)

    #skip comma separator
    parse_line_idx += 1

    p.right = __parse_element(s, p)
    
    assert s[parse_line_idx] == ']'

    #skip closing ]
    parse_line_idx += 1

    return p


def verify(s):
    assert s == str(parse_line(s))

def find_exploder(p, depth = 0):
    ret = None

    if depth == 4:
        if (
            type(p.left) == int and 
            type(p.right) == int
            ):
            ret = p
    elif depth < 4:
        if type(p.left) == Pair:
            ret = find_exploder(p.left, depth+1)
        
        if ret == None and type(p.right) == Pair:
                ret = find_exploder(p.right, depth+1)

    return ret

def find_first_number_to_the_left(p):
    pass
    p.parent


    
def __find_first_number_to_the_left(p):
    return p.parent

def explode(p):
    p = find_exploder(p)
    if p != None:
        #find first regular number to the left
        left = find_first_number_to_the_left(p)
        pass

    return p

def reduce(p):

    print('reducing:', str(p))

    #find first (left) pair at depth 4, that consists of two regular numbers, and explode it
    explode(p)

    return p

# def populate_nx_graph(g,p):

#     if p != None:

#         node_id = len(g)

#         g.add_node(node_id)

#         vals = {}

#         #Left
#         if type(p.left) == Pair:
#             child_id = populate_nx_graph(g, p.left)
#             g.add_edge(node_id, child_id, side='left')
#         else:
#             vals['left_val'] = p.left
#             g.nodes[node_id]['left_val'] = p.left
            

#         #Right
#         if type(p.right) == Pair:
#             child = populate_nx_graph(g, p.right)
#             g.add_edge(node_id, child_id, side='right')
#         else:
#             vals['right_val'] = p.right
#             g.nodes[node_id]['right_val'] = p.right

#         return node_id


def print_tree(node, level=0):
    if node != None:

        if type(node.right) == Pair:
            print_tree(node.right, level + 1)

        left_val = '_'
        if type(node.left) == int:
            left_val = node.left

        right_val = '_'
        if type(node.right) == int:
            right_val = node.right

        print(' ' * 4 * level + '->', f'({left_val},{right_val})')

        if type(node.left) == Pair:
            print_tree(node.left, level + 1)


def show_tree(p):

    print_tree(p)

    # import networkx as nx

    # g = nx.DiGraph()
    # populate_nx_graph(g, p)


    # import matplotlib.pyplot as plt
    # pos = hierarchy_pos(g,0)    
    # nx.draw(g, pos=pos, with_labels=True)
    # plt.savefig('hierarchy.png')


    # pos = graphviz_layout(g, prog="dot")
    # nx.draw(g, pos)
    # plt.show()




# filename = '2021/18_input_example.txt'
# with open(filename) as f:
#     lines = [line.strip() for line in f]

#verify('[1,2]')
verify('[[1,2],3]')
verify('[9,[8,7]]')
verify('[[1,9],[8,5]]')
verify('[[[[1,2],[3,4]],[[5,6],[7,8]]],9]')
verify('[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]')
verify('[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]')
verify('[[[[[9,8],1],2],3],4]')

show_tree((parse_line('[[[[[9,8],1],2],3],4]')))

reduce(parse_line('[[[[[9,8],1],2],3],4]'))

i = 0

