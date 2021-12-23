def read_input(filename):
    with open(filename, 'r') as f:
        return [int(num) for num in f.readline().split(',')]


positions = read_input('input.txt')
positions = sorted(positions)


def fuel_needed(positions, target_position):
    fuel = 0
    for position in positions:
        num_steps = abs(target_position - position)
        fuel += (num_steps * (num_steps + 1) / 2)
    return fuel


min_fuel = fuel_needed(positions, positions[0])
best_position = positions[0]
for target_position in range(positions[1], positions[-1]):
    fuel = fuel_needed(positions, target_position)
    if fuel < min_fuel:
        min_fuel = fuel
        best_position = target_position

print(best_position)
print(min_fuel)
