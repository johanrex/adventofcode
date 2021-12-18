
from collections import deque
import re
r = re.compile(r'\d+')


parse_line_idx = None

class Pair:
    def __init__(self) -> None:
        self.left = None
        self.right = None

    def __str__(self):
        if isinstance(self.left, Pair):
            left = str(self.left)
        else:
            left = self.left

        if isinstance(self.right, Pair):
            right = str(self.right)
        else:
            right = self.right

        s = f'[{left},{right}]'

        return s


def parse_line(s):
    global parse_line_idx
    parse_line_idx = 0 
    p = __parse_pair(s)
    return p


def __parse_element(s):
    global parse_line_idx
    e = None

    if s[parse_line_idx] == '[':
        #is pair
        e = __parse_pair(s)
    else:
        #is number
        m = r.match(s[parse_line_idx:])

        if not bool(m):
            raise Exception('expected number')

        e = m[0]

        parse_line_idx += len(e)
    
    return e


def __parse_pair(s):
    global parse_line_idx

    assert s[parse_line_idx] == '['

    p = Pair()

    #skip opening [
    parse_line_idx += 1

    p.left = __parse_element(s)

    #skip comma separator
    parse_line_idx += 1

    p.right = __parse_element(s)
    
    assert s[parse_line_idx] == ']'

    #skip closing ]
    parse_line_idx += 1

    return p


def verify(s):
    assert s == str(parse_line(s))


def reduce():
    pass


# filename = '2021/18_input_example.txt'
# with open(filename) as f:
#     lines = [line.strip() for line in f]

verify('[1,2]')
verify('[[1,2],3]')
verify('[9,[8,7]]')
verify('[[1,9],[8,5]]')
verify('[[[[1,2],[3,4]],[[5,6],[7,8]]],9]')
verify('[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]')
verify('[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]')
verify('[[[[[9,8],1],2],3],4]')


i = 0

