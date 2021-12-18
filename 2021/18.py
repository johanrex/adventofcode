
from collections import deque
import re
r = re.compile(r'\d+')

parse_line_idx = None

class Pair:
    def __init__(self) -> None:
        self.left = None
        self.right = None
        self.parent = None

    def has_left_int(self) -> bool:
        return type(self.left) == int

    def has_right_int(self) -> bool:
        return type(self.right) == int

    def has_left_child(self) -> bool:
        return not self.has_left_int()

    def has_right_child(self) -> bool:
        return not self.has_right_int()

    def __str__(self):
        str_left = str(self.left)
        str_right = str(self.right)

        s = f'[{str_left},{str_right}]'

        return s

def parse_line(s):

    print('parsing line:', s)
    
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
        if p.has_left_int() and p.has_right_int():
            ret = p
    elif depth < 4:
        if p.has_left_child():
            ret = find_exploder(p.left, depth+1)
        
        if ret == None and p.has_right_child():
                ret = find_exploder(p.right, depth+1)

    return ret

def find_first_number_to_the_left(p):
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

def print_tree(node, level=0):
    if node != None:

        if node.has_right_child():
            print_tree(node.right, level + 1)

        left_val = '_'
        if node.has_left_int():
            left_val = node.left

        right_val = '_'
        if node.has_right_int():
            right_val = node.right

        print(' ' * 4 * level + '->', f'({left_val},{right_val})')

        if node.has_left_child():
            print_tree(node.left, level + 1)


def show_tree(p):

    print_tree(p)


# filename = '2021/18_input_example.txt'
# with open(filename) as f:
#     lines = [line.strip() for line in f]

# verify('[1,2]')
# verify('[[1,2],3]')
# verify('[9,[8,7]]')
# verify('[[1,9],[8,5]]')
# verify('[[[[1,2],[3,4]],[[5,6],[7,8]]],9]')
# verify('[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]')
# verify('[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]')
# verify('[[[[[9,8],1],2],3],4]')

show_tree((parse_line('[[[[[9,8],1],2],3],4]')))

reduce(parse_line('[[[[[9,8],1],2],3],4]'))

i = 0

