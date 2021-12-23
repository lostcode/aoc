import numpy as np


# arr = np.asarray([[1, 2, 3], [2,3,4]], dtype=np.float16)
#
# arr[np.where(arr == 1)] = np.NaN
# arr[np.where(arr == 2)] = np.NaN
# arr[np.where(arr == 3)] = np.NaN


def read_input(filename):
    boards = []
    with open(filename, 'r') as f:
        numbers = [int(num) for num in f.readline().strip().split(',')]
        f.readline()  # skip

        current_board = []
        for line in f.readlines():
            if line == '\n':
                continue
            current_board.append([int(item) for item in line.lstrip(' ').split(' ') if item != ''])
            if len(current_board) == 5:
                boards.append(np.asarray(current_board, dtype=np.float32))
                current_board = []

    return numbers, boards

def is_any_row_match(board):
    # rows
    for row_arr in board:
        if np.isnan(row_arr).all():
            return True
    return False


def is_any_column_match(board):
    for i in range(0, board[0].size):
        if np.isnan(board[:, i]).all():
            return True
    return False


def mark_board(board, number):
    board[np.where(board == number)] = np.NaN
    return board


def score(numbers, boards):
    for number in numbers:
        for board in boards:
            board = mark_board(board, number)
            if is_any_row_match(board) or is_any_column_match(board):
                remaining_sum = np.nansum(board)
                return remaining_sum * number

numbers, boards = read_input('long_input.txt')
print(int(score(numbers, boards)))
