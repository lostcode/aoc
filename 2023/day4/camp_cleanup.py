
def is_overlapping(pair):
    first, second = pair
    return first[0] <= second[0] <= first[1] or second[0] <= first[0] <= second[1]


def read_interval_pairs_from_input(input_file):
    pairs = []
    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            first, second = line.split(',')
            pairs.append(((int(first.split('-')[0]), int(first.split('-')[1])), (int(second.split('-')[0]), int(second.split('-')[1]))))
    return pairs


print(sum(is_overlapping(pair) for pair in read_interval_pairs_from_input('input.txt')))

