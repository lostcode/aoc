def get_priority(char):
    if char.isupper():
        return 27 + ord(char) - ord('A')
    else:
        return 1 + ord(char) - ord('a')


def find_overlapping(items):
    return set(items[0]).intersection(set(items[1])).intersection(set(items[2])).pop()


def read_from_input():
    groups = []
    items = []
    with open('input.txt', 'r') as f:
        for line in f.readlines():
            items.append(line.strip())
            if len(items) == 3:
                groups.append(items)
                items = []
    return groups


total_priority = 0
for group in read_from_input():
    total_priority += get_priority(find_overlapping(group))

print(total_priority)
