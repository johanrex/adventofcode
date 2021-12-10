from collections import deque

def read_input(filename):
    lines = []
    with(open(filename, "r")) as f:
        for line in f:
            lines.append(list(line.strip()))
    
    return lines

lines = read_input('2021/10_input_example.txt')
lines = read_input('2021/10_input.txt')

syntax_error_score = 0
completion_scores = []

for line in lines:
    stack = deque()
    corrupted = False

    for c in line:
        if c in "([{<":
            stack.append(c)
        elif c in ")]}>":
            popped = stack.pop()
            if (
                (popped == '(' and c == ')') or
                (popped == '[' and c == ']') or
                (popped == '{' and c == '}') or
                (popped == '<' and c == '>')
                ):
                pass
            else:
                corrupted = True

                match c:
                    case ')':
                        syntax_error_score += 3
                    case ']':
                        syntax_error_score += 57
                    case '}':
                        syntax_error_score += 1197
                    case '>':
                        syntax_error_score += 25137
                    case _:
                        raise Exception('unexpected')
                break
        else:
            raise Exception('unexpected')

    if not corrupted:
        #is incomplete
        stack.reverse()
        s = ''.join(stack)
        s = s.replace('(', ')').replace('[', ']').replace('{', '}').replace('<', '>')

        completion_score = 0
        for c in s:
            completion_score *= 5

            match c:
                case ')':
                    completion_score += 1
                case ']':
                    completion_score += 2
                case '}':
                    completion_score += 3
                case '>':
                    completion_score += 4
                case _:
                    raise Exception('unexpected')            

        completion_scores.append(completion_score)

completion_scores = sorted(completion_scores)

print(f'syntax error score: ', syntax_error_score)
print(f'middle completion score: ', completion_scores[(len(completion_scores)//2)])
