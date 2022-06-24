import numpy as np


def read_input(filename):
    locations = []
    fold_instructions = []
    max_x = 0
    max_y = 0
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

        line = lines[0]
        index = 0

        while line != '':
            x = int(line.strip().split(',')[0])
            y = int(line.strip().split(',')[1])
            max_x = max(max_x, x)
            max_y = max(max_y, y)
            locations.append((x, y))
            index += 1
            line = lines[index]

        # now get fold instructions
        index += 1
        for line in lines[index:]:
            fold_str = line.strip().split('fold along ')[1]
            fold_instructions.append((fold_str.split('=')[0], fold_str.split('=')[1]))

    paper = np.zeros((max_x + 1, max_y + 1), dtype=np.bool_)
    for location in locations:
        paper[location] = True

    return np.transpose(paper), fold_instructions


paper, fold_instructions = read_input('input.txt')


def perform_fold(paper, fold_instruction):
    index = int(fold_instruction[1])
    if fold_instruction[0] == 'y':
        first_half = paper[:index, :]
        bottom_start = index + 1
        second_half = np.flipud(paper[bottom_start:, :])
        # pad horizontal top
        if paper.shape[0] % index == 0:
            second_half = np.pad(second_half, [(1, 0), (0, 0)], mode='constant', constant_values=0)
    else:
        first_half = paper[:, :index]
        right_start = index + 1
        second_half = np.fliplr(paper[:, right_start:])
        # pad vertical left
        if paper.shape[1] % index == 0:
            second_half = np.pad(second_half, [(0, 0), (1, 0)], mode='constant', constant_values=0)

    folded = first_half | second_half
    return folded


for fold_instruction in fold_instructions:
    paper = perform_fold(paper, fold_instruction)

print(np.array2string(paper, separator='', formatter={"bool": " #".__getitem__}))
