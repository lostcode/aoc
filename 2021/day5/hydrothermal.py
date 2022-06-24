import numpy as np
from dataclasses import dataclass


@dataclass
class Position:
    X: int
    Y: int


@dataclass
class Line:
    pos1: Position
    pos2: Position


def read_input(filename):
    lines = []  # only horizontal and vertical
    with open(filename, 'r') as f:
        for line in f.readlines():
            pos1 = line.split(' ')[0]
            pos2 = line.split(' ')[2]

            pos1_x = int(pos1.split(',')[0])
            pos1_y = int(pos1.split(',')[1])

            pos2_x = int(pos2.split(',')[0])
            pos2_y = int(pos2.split(',')[1])

            # only horizontal or vertical or 45 degree lines
            if pos1_x == pos2_x or pos1_y == pos2_y or (abs(pos1_x - pos2_x) == abs(pos1_y - pos2_y)):
                lines.append(Line(Position(pos1_x, pos1_y), Position(pos2_x, pos2_y)))

    return lines


def span(line):
    span_positions = []

    if line.pos1.X == line.pos2.X:
        curr_x = line.pos1.X
        for diff in range(0, abs(line.pos1.Y - line.pos2.Y) + 1):
            curr_y = line.pos1.Y + diff * (1 if line.pos1.Y < line.pos2.Y else -1)
            span_positions.append(Position(curr_x, curr_y))
        return span_positions

    if line.pos1.Y == line.pos2.Y:
        curr_y = line.pos1.Y
        for diff in range(0, abs(line.pos1.X - line.pos2.X) + 1):
            curr_x = line.pos1.X + diff * (1 if line.pos1.X < line.pos2.X else -1)
            span_positions.append(Position(curr_x, curr_y))
        return span_positions

    # 45 degree case
    for diff in range(0, abs(line.pos1.X - line.pos2.X) + 1):
        curr_x = line.pos1.X + diff * (1 if line.pos1.X < line.pos2.X else -1)
        curr_y = line.pos1.Y + diff * (1 if line.pos1.Y < line.pos2.Y else -1)
        span_positions.append(Position(curr_x, curr_y))

    return span_positions


lines = read_input('long_input.txt')

grid = np.empty((1000, 1000))
grid[:] = 0

for line in lines:
    span_positions = span(line)
    for pos in span_positions:
        grid[pos.X, pos.Y] += 1


print(np.count_nonzero(grid >= 2))
