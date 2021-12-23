import numpy as np
from scipy.ndimage import label


def read_input(filename):
    with open(filename, 'r') as f:
        height_map = []
        for line in f.readlines():
            height_map.append([int(item) for item in line.strip()])

    return np.asarray(height_map, dtype=np.float32)


def find_low_points(height_map):
    low_points = []
    for i in range(height_map.shape[0]):
        for j in range(height_map.shape[1]):
            curr = height_map[i, j]
            if i - 1 >= 0:
                if curr >= height_map[i - 1, j]:
                    continue
            if i + 1 < height_map.shape[0]:
                if curr >= height_map[i + 1, j]:
                    continue
            if j - 1 >= 0:
                if curr >= height_map[i, j - 1]:
                    continue
            if j + 1 < height_map.shape[1]:
                if curr >= height_map[i, j + 1]:
                    continue

            low_points.append(curr)

    return low_points


def pre_discover(height_map, i, j, target):
    height_map[i, j] = target
    if i - 1 >= 0 and np.isnan(height_map[i - 1, j]):
        pre_discover(height_map, i - 1, j, target)
    if i + 1 < height_map.shape[0] and np.isnan(height_map[i + 1, j]):
        pre_discover(height_map, i + 1, j, target)
    if j - 1 >= 0 and np.isnan(height_map[i, j - 1]):
        pre_discover(height_map, i, j - 1, target)
    if j + 1 < height_map.shape[1] and np.isnan(height_map[i, j + 1]):
        pre_discover(height_map, i, j + 1, target)

    return height_map


def find_basins(height_map):
    discovered = 10
    for i in range(height_map.shape[0]):
        for j in range(height_map.shape[1]):
            curr = height_map[i, j]
            if curr == 9:
                continue
            if i - 1 >= 0:
                if not np.isnan(height_map[i - 1, j]) and height_map[i - 1, j] != 9:
                    pre_discover(height_map, i, j, height_map[i - 1, j])
                    continue
            if i + 1 < height_map.shape[0]:
                if not np.isnan(height_map[i + 1, j]) and height_map[i + 1, j] != 9:
                    pre_discover(height_map, i, j, height_map[i + 1, j])
                    continue
            if j - 1 >= 0:
                if not np.isnan(height_map[i, j - 1]) and height_map[i, j - 1] != 9:
                    pre_discover(height_map, i, j, height_map[i, j - 1])
                    continue
            if j + 1 < height_map.shape[1]:
                if not np.isnan(height_map[i, j + 1]) and height_map[i, j + 1] != 9:
                    pre_discover(height_map, i, j, height_map[i, j + 1])
                    continue
            # undiscovered
            pre_discover(height_map, i, j, discovered)
            discovered += 1

    return height_map, discovered


def find_mul_3_largest_basins(discovered_height_map, max_discovered):
    all_basins = []
    for discovered in range(10, max_discovered):
        all_basins.append(np.count_nonzero(discovered_height_map == discovered))

    num_counted = 0
    mul = 1
    for num_locations in sorted(all_basins, reverse=True):
        if num_counted == 3:
            break
        mul *= num_locations
        num_counted += 1

    return mul


def prod_three_largest_basins(height_map):
    height_map[height_map != 9] = np.NaN
    discovered_height_map, max_discovered = find_basins(height_map)
    return find_mul_3_largest_basins(discovered_height_map, max_discovered)


print(prod_three_largest_basins(read_input('long_input.txt')))


# much more concise way of doing it using scipy 'label' and inverting the height map
# it's the same general idea as the previous code, just far more elegant and short!
# np.partition gives a fast (partial) sort to find largest N elements
def find_three_largest_basins(height_map):
    labeled, _ = label(9 - height_map)
    _, counts = np.unique(labeled[labeled != 0], return_counts=True)
    return -np.partition(-counts, 3)[:3]


print(np.prod(find_three_largest_basins(read_input('long_input.txt'))))

