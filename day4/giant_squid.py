import numpy as np


# ------------
# noteworthy
# ------------
#
# to prevent throwing off the later indices, when removing multiple indices from a list, use
#   for index in sorted(indices, reverse=True)
#     del list[index]
#
# np.nansum(array) => to find total sum ignoring nans
#
# np.isnan(array).all() => to find if all elements in an array are nans
#
# array[np.where(array == number)] = np.NaN => to set all items equal to 'number' as NaN
#

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
        board_indexes_to_delete = []
        for i, board in enumerate(boards):
            board = mark_board(board, number)
            if is_any_row_match(board) or is_any_column_match(board):
                if len(boards) == 1:
                    remaining_sum = np.nansum(board)
                    return remaining_sum * number
                else:
                    board_indexes_to_delete.append(i)

        # clear boards
        for i in sorted(board_indexes_to_delete, reverse=True):
            del boards[i]

numbers, boards = read_input('long_input.txt')
print(int(score(numbers, boards)))

