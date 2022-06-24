import numpy as np


def power_level(serial, x, y) -> int:
    rack_id = x + 10
    power = rack_id * y
    power += serial
    power *= rack_id
    power = power // 100
    power = power % 10
    power -= 5
    return power


assert power_level(8, 3, 5) == 4
assert power_level(57, 122, 79) == -5
assert power_level(39, 217, 196) == 0
assert power_level(71, 101, 153) == 4


def populate_grid(serial):
    grid = np.zeros((301, 301), dtype=np.int32)
    for x in range(0, grid.shape[0]):
        for y in range(0, grid.shape[1]):
            grid[(x, y)] = power_level(serial, x, y)
    return grid


def total_power(grid, top_left_x, top_left_y, size=3):
    total = 0
    for x in range(top_left_x, top_left_x + size):
        for y in range(top_left_y, top_left_y + size):
            total += grid[(x, y)]
    return total


memoized = {}


def total_power_incremental(grid, top_left_x, top_left_y, size):
    total = memoized[(top_left_x, top_left_y, size - 1)]
    total += grid[top_left_x : top_left_x + size - 1, top_left_y + size - 1].sum()
    total += grid[top_left_x + size - 1, top_left_y : top_left_y + size - 1].sum()
    memoized[(top_left_x, top_left_y, size)] = total
    del memoized[(top_left_x, top_left_y, size - 1)]
    return total


def bootstrap_power(grid):
    for x in range(0, grid.shape[0]):
        for y in range(0, grid.shape[1]):
            memoized[(x, y, 1)] = grid[(x, y)]


def find_max_power(grid, size=3):
    max_power, max_x, max_y = 0, 0, 0
    for x in range(0, grid.shape[0] - size):
        for y in range(0, grid.shape[1] - size):
            total = total_power(grid, x, y, size)
            if total > max_power:
                max_power = total
                max_x, max_y = x, y

    return max_power, max_x, max_y


def find_max_power_incremental(grid, final_size=3):
    bootstrap_power(grid)
    max_power, max_x, max_y, max_size = 0, 0, 0, 0
    for size in range(2, final_size + 1):
        print("computing size = ", size)
        for x in range(0, grid.shape[0] - size):
            for y in range(0, grid.shape[1] - size):
                total = total_power_incremental(grid, x, y, size)
                if total > max_power:
                    max_power = total
                    max_x, max_y = x, y
                    max_size = size

    return max_power, max_x, max_y, max_size


# grid = populate_grid(serial=18)
# print(total_power(grid, 33, 45))

# grid = populate_grid(serial=42)
# print(grid[(33, 45)])
# print(total_power(grid, 21, 61))

grid = populate_grid(serial=7857)
max_power, max_x, max_y, max_size = find_max_power_incremental(grid, final_size=300)
print(max_power, max_x, max_y, max_size)
