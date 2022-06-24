import sys
from collections import defaultdict
from heapq import heappush, heappop
from typing import List

import numpy as np

graph = np.genfromtxt('input.txt', dtype=np.uint8, delimiter=1)


def new_tile_row(graph):
    tile_row = graph.copy()
    next_tile = tile_row.copy()  # original map tile
    for i in range(4):
        next_tile += 1
        next_tile[next_tile == 10] = 1
        tile_row = np.concatenate((tile_row, next_tile), axis=1)
    return tile_row


def full_map(graph):
    full_graph = None
    for i in range(5):
        row = new_tile_row(graph)
        if full_graph is None:
            full_graph = row
        else:
            full_graph = np.vstack((full_graph, row))
        graph += 1
        graph[graph == 10] = 1
    return full_graph


graph = full_map(graph)


class Node:
    def __init__(self, x=0, y=0, risk=0):
        self.x = x
        self.y = y
        self.risk = risk

    def __repr__(self):
        return "Node({}, {}, {})".format(self.x, self.y, self.risk)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def outgoing(node: Node, graph) -> List[Node]:
    outgoing_nodes = []
    for pos in ((node.x - 1, node.y), (node.x + 1, node.y), (node.x, node.y - 1), (node.x, node.y + 1)):
        if (0 <= pos[0] < graph.shape[0]) and (0 <= pos[1] < graph.shape[1]):
            outgoing_nodes.append(Node(pos[0], pos[1], graph[pos]))
    return outgoing_nodes


# dijkstra's
def compute_shortest_paths(graph, start_node, target_node):

    shortest_paths = defaultdict(lambda: sys.maxsize)
    shortest_paths[(start_node.x, start_node.y)] = 0
    to_visit_pq = [(0, start_node)]

    while to_visit_pq:
        node = heappop(to_visit_pq)[-1]
        if node == target_node:
            return shortest_paths
        for outgoing_node in outgoing(node, graph):
            new_distance = shortest_paths[(node.x, node.y)] + outgoing_node.risk
            if new_distance < shortest_paths[(outgoing_node.x, outgoing_node.y)]:
                shortest_paths[(outgoing_node.x, outgoing_node.y)] = new_distance
                heappush(to_visit_pq, (new_distance, id(outgoing_node), outgoing_node))

    return shortest_paths


start_node = Node(0, 0, graph[0, 0])
target_node = Node(graph.shape[0] - 1, graph.shape[1] - 1, graph[graph.shape[0] - 1, graph.shape[1] - 1])

shortest_paths = compute_shortest_paths(graph, start_node, target_node)
print(shortest_paths)
print(shortest_paths[(target_node.x, target_node.y)])
