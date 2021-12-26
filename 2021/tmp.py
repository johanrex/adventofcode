
class BinaryTreeNode():
    def __init__(self) -> None:
        self.left_value = None
        self.right_value = None
        self.left_child = None
        self.right_child = None
        self.parent = None

    def __str__(self) -> str:
        
        if self.left_value is not None:
            left_part = self.left_value
        elif self.left_child is not None:
            left_part = str(self.left_child)

        if self.right_value is not None:
            right_part = self.right_value
        elif self.right_child is not None:
            right_part = str(self.right_child)

        return f'[{left_part},{right_part}]'


    def get_dfs_list(self):
        node_list = []

        self.__get_dfs_list(node_list, self)

        return node_list

    def __get_dfs_list(self, node_list, node):

        if node.left_child is not None:
            self.__get_dfs_list(node_list, node.left_child)

        node_list.append(node)

        if node.right_child is not None:
            self.__get_dfs_list(node_list, node.right_child)


    def get_levels(self):
        levels_nodes = {}
        self.__get_levels(levels_nodes, self)
        return levels_nodes

    def __get_levels(self, levels_nodes:dict, node: 'BinaryTreeNode', level:int=1):
        if node is None:
            return 

        self.__get_levels_add_node(levels_nodes, node, level)
        
        if node.left_child is not None:
            self.__get_levels(levels_nodes, node.left_child, level+1)
        if node.right_child is not None:
            self.__get_levels(levels_nodes, node.right_child, level+1)

    def __get_levels_add_node(self, levels_nodes, node, level):
        if not level in levels_nodes:
            levels_nodes[level] = []
       
        levels_nodes[level].append(node)

    def pretty_print(self):
        levels_nodes = self.get_levels()
       
        levels = sorted(levels_nodes.keys())
        nr_of_levels = len(levels)
        max_nodes_on_last_level = 2 **nr_of_levels
        length_per_node = len('(None,None')
        length_longest_level = length_per_node * max_nodes_on_last_level

        for level in levels:
            nodes = levels_nodes[level]
            s = f'Level: {level}{(nr_of_levels-level) * " "}'
            for node in nodes:

                s += f'({node.left_value},{node.right_value})'
            print(s)


    @staticmethod
    def from_json(json_str):
        import json
        data = json.loads(json_str)
        node = BinaryTreeNode.__from_json_dfs(data)

        assert json_str == str(node)

        return node


    @staticmethod
    def __from_json_dfs(node_json, parent = None):

        node = BinaryTreeNode()
        node.parent = parent

        #left
        if type(node_json[0]) == int:
            node.left_value = node_json[0]
        else:
            if type(node_json[0]) == list:
                node.left_child = BinaryTreeNode.__from_json_dfs(node_json[0], node)
            else:
                raise Exception('unexpected')

        #right
        if type(node_json[1]) == int:
            node.right_value = node_json[1]
        else:
            if type(node_json[1]) == list:
                node.right_child = BinaryTreeNode.__from_json_dfs(node_json[1], node)
            else:
                raise Exception('unexpected')

        return node


def explode(root: BinaryTreeNode):
    
    exploded = False

    levels_nodes = root.get_levels()
    if 5 in levels_nodes:
        exploded = True

        nodes = levels_nodes[5]
        leftmost_4_level_deep = nodes[0]

        lst = root.get_dfs_list()
        idx = lst.index(leftmost_4_level_deep)

        if (idx > 0) and leftmost_4_level_deep.left_value is not None:
            for prev in reversed(lst[0:idx]):
                if prev.right_value is not None:
                    prev.right_value += leftmost_4_level_deep.left_value
                    break
                elif prev.left_value is not None:
                    prev.left_value += leftmost_4_level_deep.left_value
                    break

        if (idx < len(lst)-1) and leftmost_4_level_deep.right_value is not None:
            for next in lst[idx+1:]:
                if next.left_value is not None:
                    next.left_value += leftmost_4_level_deep.right_value
                    break
                elif next.right_value is not None:
                    next.right_value += leftmost_4_level_deep.right_value
                    break

        #set to 0
        parent = leftmost_4_level_deep.parent
        if parent.left_child == leftmost_4_level_deep:
            parent.left_child = None
            parent.left_value = 0
        elif parent.right_child == leftmost_4_level_deep:
            parent.right_child = None
            parent.right_value = 0

        print('after explode:', str(root))

    return exploded


def split_value_to_node(val_to_split, parent):
    new_left_val = val_to_split // 2
    new_right_val = val_to_split - new_left_val

    new_node = BinaryTreeNode()
    new_node.parent = parent
    new_node.left_value = new_left_val
    new_node.right_value = new_right_val

    return new_node


def split(root: BinaryTreeNode):

    splitted = False
    lst = root.get_dfs_list()

    for node in lst:

        if node.left_value is not None and node.left_value >= 10:
            node.left_child = split_value_to_node(node.left_value, node)
            node.left_value = None
            splitted = True
            break

        elif node.right_value is not None and node.right_value >= 10:
            node.right_child = split_value_to_node(node.right_value, node)
            node.right_value = None
            splitted = True
            break

    if splitted:
        print('after split:', str(root))

    return splitted


def reduce(root: BinaryTreeNode):
    
    while True:
        if explode(root):
            continue

        if split(root):
            continue

        break


def test_reduce(input, output):
    node = BinaryTreeNode.from_json(input)
    reduce(node)
    
    assert str(node) == output


def test_explode(input, output):
    node = BinaryTreeNode.from_json(input)
    explode(node) 

    assert str(node) == output


def tests():
    strs = [
        '[1,2]',
        '[[1,2],3]',
        '[9,[8,7]]',
        '[[1,9],[8,5]]',
        '[[[[1,2],[3,4]],[[5,6],[7,8]]],9]',
        '[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]',
        '[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]',
        '[[[[[9,8],1],2],3],4]',
        '[7,[6,[5,[4,[3,2]]]]]',
        '[[6,[5,[4,[3,2]]]],1]',
        '[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]',
        '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]'
    ]

    for s in strs:
        assert s == str(BinaryTreeNode.from_json(s))

    test_explode('[[[[[9,8],1],2],3],4]', '[[[[0,9],2],3],4]')
    test_explode('[7,[6,[5,[4,[3,2]]]]]', '[7,[6,[5,[7,0]]]]')
    test_explode('[[6,[5,[4,[3,2]]]],1]', '[[6,[5,[7,0]]],3]')
    test_explode('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]', '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')
    test_explode('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]', '[[3,[2,[8,0]]],[9,[5,[7,0]]]]')

    test_reduce('[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]', '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]')

tests()

print('Input:')
json_str = '[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]'
print(json_str)
root = BinaryTreeNode.from_json(json_str)

reduce(root)

i = 0

# pp = BinaryTreePrettyPrinter()
# pp.pretty_print(data)

