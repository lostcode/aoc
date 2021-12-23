import numpy as np
from collections import Counter


def read_input(filename):
    with open(filename, 'r') as f:
        return np.asarray([int(num) for num in f.readline().split(',')], dtype=np.int16)


# mega slow for part 2!
def simulate(lanternfish, num_days):
    for i in range(1, num_days + 1):
        zeros_mask = lanternfish == 0
        num_append = np.count_nonzero(zeros_mask)
        lanternfish[~zeros_mask] -= 1
        lanternfish[zeros_mask] = 6
        lanternfish = np.append(lanternfish, num_append * [8])

    return lanternfish


lanternfish = np.asarray(read_input('input.txt'))
rem_days_dict = Counter(lanternfish)
num_days = 256
for i in range(1, num_days + 1):
    num_new_fish = rem_days_dict[0]

    for j in range(0, 8):
        rem_days_dict[j] = rem_days_dict[j+1]

    rem_days_dict[6] += num_new_fish
    rem_days_dict[8] = num_new_fish

print(sum(rem_days_dict.values()))


