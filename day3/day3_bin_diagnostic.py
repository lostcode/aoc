import numpy as np

#
# ----------------
# salient features
# ----------------
#
# np.asarray(...) to convert from a list of lists to a 2D array
#
# nparray[:, column_index] => get a column vector from a 2D array
#
# np.bincount(column_vector) => get a histogram
#
# argmax() => index with the maximum value
#
# number << 1 | bit => append a bit to the end of a number
#


def read_input(filename):
    numbers_list = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            arr = []
            for char in line.strip():
                arr.append(int(char))

            numbers_list.append(arr)
    return numbers_list


def get_rates(numbers):
    gamma_rate = 0
    epsilon_rate = 0
    for col_index in range(numbers[0].size):
        column_bits = numbers[:, col_index]
        argmax_index = np.bincount(column_bits).argmax()
        max_bit = argmax_index  # bin number
        gamma_rate = gamma_rate << 1 | max_bit
        min_bit = 1 - max_bit
        epsilon_rate = epsilon_rate << 1 | min_bit

    return gamma_rate, epsilon_rate


gamma_rate, epsilon_rate = get_rates(np.asarray(read_input('day3_long_input.txt')))
print(gamma_rate * epsilon_rate)
