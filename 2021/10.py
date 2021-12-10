from collections import deque

def read_input(filename):
    lines = []
    with(open(filename, "r")) as f:
        for line in f:
            lines.append(list(line.strip()))
    
    return lines

#lines = read_input('2021/10_input_example.txt')
lines = read_input('2021/10_input.txt')

correct_lines = 0
corrupted_lines = 0
incomplete_lines = 0

syntax_error_score = 0


for line in lines:
    stack = deque()

    for c in line:
        if c in "([{<":
            stack.append(c)
        elif c in ")]}>":
            popped = stack.pop()
            if popped == '(' and c == ')':
                pass
            elif popped == '[' and c == ']':
                pass
            elif popped == '{' and c == '}':
                pass
            elif popped == '<' and c == '>':
                pass
            else:

                if c == ')':
                    syntax_error_score += 3
                elif c == ']':
                    syntax_error_score += 57
                elif c == '}':
                    syntax_error_score += 1197
                elif c == '>':
                    syntax_error_score += 25137

                corrupted_lines += 1
                break
        else:
            raise Exception('unexpected')

    if len(stack) == 0:
        correct_lines += 1
    else:
        incomplete_lines += 1

print(f'correct lines: ', correct_lines)
print(f'corrupted lines: ', corrupted_lines)
print(f'incomplete lines: ', incomplete_lines)
print(f'syntax error score: ', syntax_error_score)
