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


def number_from_bits(bit_array):
    numbers = 0
    for bit in bit_array:
        numbers = numbers << 1 | bit
    return numbers


def most_common(column_vector):
    bincounts = np.bincount(column_vector)
    assert len(bincounts) == 2
    if bincounts[0] == bincounts[1]:
        return -1
    else:
        return 0 if bincounts[0] > bincounts[1] else 1


def trim(numbers, index, o2=True):
    column_bits = numbers[:, index]  # look at first bit
    max_bit = most_common(column_bits)
    if max_bit == -1:
        priority_bit = 1 if o2 else 0
    else:
        priority_bit = max_bit if o2 else 1 - max_bit
    return numbers[np.where(column_bits == priority_bit)]


def rating(numbers, o2=True):
    for index in range(0, numbers[0].size):
        numbers = trim(numbers, index, o2)
        if len(numbers) == 1:
            return number_from_bits(numbers[0])


def get_rates(numbers):
    gamma_rate = 0
    epsilon_rate = 0
    for col_index in range(numbers[0].size):
        column_bits = numbers[:, col_index]
        max_bit = most_common(column_bits)
        gamma_rate = gamma_rate << 1 | max_bit
        min_bit = 1 - max_bit
        epsilon_rate = epsilon_rate << 1 | min_bit

    return gamma_rate, epsilon_rate


# part 2
numbers = np.asarray(read_input('day3_long_input.txt'))
o2_rating = rating(numbers)
co2_rating = rating(numbers, o2=False)
print(o2_rating * co2_rating)

# part 1
gamma_rate, epsilon_rate = get_rates(np.asarray(read_input('day3_short_input.txt')))
print(gamma_rate * epsilon_rate)
