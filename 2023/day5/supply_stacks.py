from typing import List, Deque
from collections import deque


def run_instructions(stacks: List[Deque], instructions):
    for instr in instructions:
        items = []
        for i in range(instr[0]):  # number of times to move
            items.append(stacks[instr[1] - 1].pop())
        stacks[instr[2] - 1].extend(reversed(items))


def read_instructions_from_file():
    instructions = []
    with open('input.txt') as f:
        for line in f.readlines():
            line = line.strip()
            num_to_move, from_stack, to_stack = line.split(' ')
            instructions.append((int(num_to_move), int(from_stack), int(to_stack)))
    return instructions


def get_top_items(stacks: List[Deque]):
    top_items = ''
    for stack in stacks:
        top_items += stack[-1]
    return top_items


stacks = []
stacks.append(deque(['R', 'C', 'H']))
stacks.append(deque(['F', 'S', 'L', 'H', 'J', 'B']))
stacks.append(deque(['Q', 'T', 'J', 'H', 'D', 'M', 'R']))
stacks.append(deque(['J', 'B', 'Z', 'H', 'R', 'G', 'S']))
stacks.append(deque(['B', 'C', 'D', 'T', 'Z', 'F', 'P', 'R']))
stacks.append(deque(['G', 'C', 'H', 'T']))
stacks.append(deque(['L', 'W', 'P', 'B', 'Z', 'V', 'N', 'S']))
stacks.append(deque(['C', 'G', 'Q', 'J', 'R']))
stacks.append(deque(['S', 'F', 'P', 'H', 'R', 'T', 'D', 'L']))
for stack in stacks:
    stack = stack.reverse()

run_instructions(stacks, read_instructions_from_file())

print(get_top_items(stacks))