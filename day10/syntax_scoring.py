from collections import deque
import statistics

open_close_map = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

score_map = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

incomplete_score_map = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


def read_input(filename):
    with open(filename, 'r') as f:
        chunks = [line.strip() for line in f.readlines()]
    return chunks


def first_illegal_character(s):
    close_queue = deque()
    for bracket in s:
        if bracket in open_close_map.keys():  # open bracket
            close_queue.appendleft(open_close_map[bracket])
        else:
            # got a close bracket
            if not close_queue:
                raise Exception('unexpected')
            expected_close_bracket = close_queue.popleft()
            if expected_close_bracket != bracket:
                return bracket
    return None


def get_incomplete_chars(s):
    close_queue = deque()
    for bracket in s:
        if bracket in open_close_map.keys():  # open bracket
            close_queue.appendleft(open_close_map[bracket])
        else:
            # got a close bracket
            if not close_queue:
                raise Exception('unexpected')
            expected_close_bracket = close_queue.popleft()
            if expected_close_bracket != bracket:
                return None  # illegal, don't care

    if close_queue:
        return close_queue  # incomplete chars

    return None


def incomplete_score(close_queue):
    score = 0
    while close_queue:
        score *= 5
        score += incomplete_score_map[close_queue.popleft()]
    return score


def get_incomplete_chunk_score(chunks):
    incomplete_chunk_scores = []
    for chunk in chunks:
        incomplete_chars = get_incomplete_chars(chunk)
        if incomplete_chars:
            incomplete_chunk_scores.append(incomplete_score(incomplete_chars))

    return statistics.median(incomplete_chunk_scores)


print(get_incomplete_chunk_score(read_input('long_input.txt')))
