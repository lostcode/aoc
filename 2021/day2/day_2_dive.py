def read_input(filename):
    commands = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            direction = line.split(' ')[0]
            amount = int(line.split(' ')[1])
            commands.append((direction, amount))
    return commands


def positions(commands):
    aim_position = 0
    horizontal_position = 0
    depth_position = 0
    for direction, amount in commands:
        if direction == 'forward':
            depth_position += (amount * aim_position)
            horizontal_position += amount
        if direction == 'up':
            aim_position -= amount
        if direction == 'down':
            aim_position += amount
    return horizontal_position, depth_position


def final_position(positions):
    return positions[0] * positions[1]


print(final_position(positions(read_input('day_2_long_input.txt'))))
