from collections import Counter


def read_input(filename):
    rules = {}

    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    template = lines[0]
    for line in lines[2:]:
        rules[line.split(' -> ')[0]] = line.split(' -> ')[1]

    return template, rules


template, rules = read_input('input.txt')


def extend(template, rules):
    new_template = template[0]
    for i in range(0, len(template) - 1):
        new_template += rules[template[i:i + 2]] + template[i + 1]

    return new_template, pair_counter


def extend_using_counters(pair_counter, word_counter, rules):
    new_pair_counter = Counter()

    for pair, num_times in pair_counter.items():
        insert_element = rules[pair]
        new_pair_counter[pair[0] + insert_element] += num_times
        new_pair_counter[insert_element + pair[1]] += num_times
        word_counter[insert_element] += num_times

    return new_pair_counter, word_counter


num_steps = 40
pair_counter = Counter()
for i in range(0, len(template) - 1):
    pair_counter[template[i:i + 2]] += 1

word_counter = Counter(template)

for step in range(1, num_steps + 1):
    pair_counter, word_counter = extend_using_counters(pair_counter, word_counter, rules)

sorted_counts = Counter(word_counter).most_common()
print(sorted_counts[0][1] - sorted_counts[-1][1])
