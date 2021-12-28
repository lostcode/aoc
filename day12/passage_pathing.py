from collections import defaultdict, deque, Counter


def read_input(filename):
    edges = defaultdict(list)
    with open(filename, 'r') as f:
        for line in f.readlines():
            node1 = line.strip().split('-')[0]
            node2 = line.strip().split('-')[1]
            if node1 == 'start':
                edges['start'].append(node2)
            elif node2 == 'start':
                edges['start'].append(node1)
            elif node1 == 'end':
                edges[node2].append(node1)
            elif node2 == 'end':
                edges[node1].append(node2)
            else:
                edges[node1].append(node2)
                edges[node2].append(node1)
    return edges


edges = read_input('input.txt')

to_visit = deque()
to_visit.append('start')


def has_visited_small_cave(curr_node, visited, max_visits=2):
    if curr_node == 'start' or curr_node == 'end':
        return False
    if curr_node.islower():
        if max_visits in visited.values():  # already visited small cave twice
            return visited[curr_node] > 0
    return False


def visit(edges, curr_node, visited):
    paths = []
    if curr_node == 'end':
        return [['end']]
    new_visited = visited.copy()
    if curr_node.islower():
        new_visited[curr_node] += 1
    for node in edges[curr_node]:
        if has_visited_small_cave(node, new_visited):
            continue
        for path in visit(edges, node, new_visited):
            paths.append([curr_node] + path)
    return paths


all_paths = visit(edges, 'start', Counter())
print(len(all_paths))
