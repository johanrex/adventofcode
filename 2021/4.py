import common

def parse_board(lines):
    numbers = []

    for line in lines:
        row = list(map(int, line.split()))
        numbers.append(row)

    return numbers

def parse_boards(input):

    boards = []

    start_idx = 2

    while start_idx <= len(input):
        end_idx = start_idx + 5

        board = input[start_idx:end_idx]

        board = parse_board(board)
        boards.append(board)

        start_idx += 6

    return boards

def is_winning_board(board, row_idx, col_idx):
    row = board[row_idx]
    win_row = row.count(None) == 5

    #transpose matrix
    t_board = list(zip(*board))
    col = t_board[col_idx]
    win_col = col.count(None) == 5

    return win_row or win_col

def find_winning_board(orders, boards):
    for order in orders:
        for board in boards:
            for row_idx in range(5):
                for col_idx in range(5):
                    if order == board[row_idx][col_idx]:
                        board[row_idx][col_idx] = None
                        if is_winning_board(board, row_idx, col_idx) == True:
                            return order, board

    #Not expected to happen
    return None

def score_board(order, board):
    numbers_left = []
    for row in board:
        for num in row:
            if num != None:
                numbers_left.append(num)

    numbers_left_sum = sum(numbers_left)
    final_score = order * numbers_left_sum
    return final_score

def part1(input_file):

    input = common.read_file(input_file)
    orders = list(map(int, input[0].split(sep=',')))

    boards = parse_boards(input)

    order, win_board = find_winning_board(orders, boards)

    final_score = score_board(order, win_board)

    print(f'final score: {final_score}')

#find_score('2021/4_input_test.txt')
part1('2021/4_input.txt')


i=0