from itertools import permutations
import math
from typing import Union


class Pair:
    left: Union['Pair', int]
    right: Union['Pair', int]
    parent: Union['Pair', None]

    def __init__(self, left, right, parent) -> None:
        self.left = left
        self.right = right
        self.parent = parent

    def __repr__(self) -> str:
        return 'Pair(l={}, r={})'.format(self.left, self.right)

    @staticmethod
    def from_array(arr, parent=None) -> 'Pair':
        pair = Pair(None, None, parent)
        pair.left = arr[0] if not isinstance(arr[0], list) else Pair.from_array(arr[0], pair)
        pair.right = arr[1] if not isinstance(arr[1], list) else Pair.from_array(arr[1], pair)
        return pair

    @staticmethod
    def to_array(pair: 'Pair'):
        if isinstance(pair.left, int) and isinstance(pair.right, int):
            return [pair.left, pair.right]
        elif isinstance(pair.left, int):
            return [pair.left, Pair.to_array(pair.right)]
        elif isinstance(pair.right, int):
            return [Pair.to_array(pair.left), pair.right]
        else:
            return [Pair.to_array(pair.left), Pair.to_array(pair.right)]

    def is_leaf_pair(self):
        return isinstance(self.left, int) and isinstance(self.right, int)


def update_leftmost_atleast_10(pair) -> bool:

    did_update = False
    if isinstance(pair.left, int):
        if pair.left >= 10:
            pair.left = Pair(math.floor(pair.left / 2), math.ceil(pair.left / 2), pair)
            return True
    else:
        did_update = update_leftmost_atleast_10(pair.left)

    if not did_update:
        if isinstance(pair.right, int):
            if pair.right >= 10:
                pair.right = Pair(math.floor(pair.right / 2), math.ceil(pair.right / 2), pair)
                return True
        else:
            did_update = update_leftmost_atleast_10(pair.right)

    return did_update


def find_leftmost_depth_4_pair(pair, depth=4):

    if pair.is_leaf_pair():
        assert depth >= 0
        return pair if depth == 0 else None

    if isinstance(pair.left, Pair):
        left_pair = find_leftmost_depth_4_pair(pair.left, depth - 1)
        if left_pair:
            return left_pair

    if isinstance(pair.right, Pair):
        right_pair = find_leftmost_depth_4_pair(pair.right, depth - 1)
        if right_pair:
            return right_pair

    return None


def update_highest_left_child(pair, value):
    if isinstance(pair.left, int):
        pair.left += value
    else:
        return update_highest_left_child(pair.left, value)


def update_highest_right_child(pair, value):
    if isinstance(pair.right, int):
        pair.right += value
    else:
        update_highest_right_child(pair.right, value)


def update_left_adjacent(pair, value):
    if pair.parent is None:
        return
    if isinstance(pair.parent.left, int):
        pair.parent.left += value
    elif pair.parent.left is pair:
        update_left_adjacent(pair.parent, value)
    else:
        update_highest_right_child(pair.parent.left, value)


def update_right_adjacent(pair, value):
    if pair.parent is None:
        return
    if isinstance(pair.parent.right, int):
        pair.parent.right += value
    elif pair.parent.right is pair:
        update_right_adjacent(pair.parent, value)
    else:
        update_highest_left_child(pair.parent.right, value)


def explode(pair):
    assert isinstance(pair.left, int)
    assert isinstance(pair.right, int)
    update_left_adjacent(pair, pair.left)
    update_right_adjacent(pair, pair.right)
    if pair is pair.parent.right:
        pair.parent.right = 0
    elif pair is pair.parent.left:
        pair.parent.left = 0
    else:
        raise Exception('unexpected')


def update_leftmost_depth_4_pair(pair):
    leftmost_pair = find_leftmost_depth_4_pair(pair)
    if leftmost_pair:
        explode(leftmost_pair)


def add(pair1, pair2) -> Pair:
    new_root = Pair(pair1, pair2, None)
    pair1.parent = new_root
    pair2.parent = new_root
    return new_root


def routine(pair1, pair2):
    root = add(pair1, pair2)

    while True:
        leftmost_pair = find_leftmost_depth_4_pair(root)
        if leftmost_pair:
            explode(leftmost_pair)
        else:
            did_update = update_leftmost_atleast_10(root)
            if not did_update:
                break
    return root


def magnitude(pair) -> int:
    if pair.is_leaf_pair():
        return 3 * pair.left + 2 * pair.right
    elif isinstance(pair.left, int):
        return 3 * pair.left + 2 * magnitude(pair.right)
    elif isinstance(pair.right, int):
        return 3 * magnitude(pair.left) + 2 * pair.right
    else:
        return 3 * magnitude(pair.left) + 2 * magnitude(pair.right)


assert magnitude(Pair.from_array([[1,2],[[3,4],5]])) == 143
assert magnitude(Pair.from_array([[[[0,7],4],[[7,8],[6,0]]],[8,1]])) == 1384
assert magnitude(Pair.from_array([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]])) == 3488


def read_input(filename):
    with open(filename, 'r') as f:
        return [eval(line.strip()) for line in f.readlines()]


input = read_input('test_input.txt')

# root = Pair.from_array(input[0])
# for num in input[1:]:
#     root = routine(root, Pair.from_array(num))
#     # print(Pair.to_array(root))
#
# print(Pair.to_array(root))
# print(magnitude(root))

highest_magnitude = max(magnitude(routine(Pair.from_array(left_arr), Pair.from_array(right_arr)))
                        for left_arr, right_arr in permutations(input, 2))
print(highest_magnitude)

