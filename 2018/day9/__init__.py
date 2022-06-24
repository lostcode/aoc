from collections import defaultdict

marbles = []


class Marble:
    def __init__(self, value) -> None:
        self.value = value
        self.next = self
        self.prev = self


start = Marble(0)


def turn(current: Marble, number: int) -> Marble:
    next_1 = current.next
    next_2 = next_1.next
    new_marble = Marble(number)
    next_1.next = new_marble
    new_marble.next = next_2
    new_marble.prev = next_1
    next_2.prev = new_marble
    return new_marble


def special_turn(current: Marble) -> (Marble, Marble):
    to_remove = current
    for i in range(7):
        to_remove = to_remove.prev

    # "remove" the node
    to_remove.prev.next = to_remove.next
    to_remove.next.prev = to_remove.prev

    current = to_remove.next

    return to_remove, current


def run(last_marble_value: int, num_players: int):
    scores = defaultdict(int)
    current_marble = start
    next_marble_value = 1
    while True:
        for player in range(num_players):
            if next_marble_value > last_marble_value:
                return scores
            if next_marble_value % 23 == 0:
                to_remove, current_marble = special_turn(current_marble)
                scores[player] += to_remove.value
                scores[player] += next_marble_value
            else:
                current_marble = turn(current_marble, next_marble_value)

            next_marble_value += 1


def get_highest_score(scores: dict) -> int:
    return max(scores.values())


# num_players = 10
# last_marble_value = 1618
# scores = run(last_marble_value, num_players)
# print(scores)
# print(get_highest_score(scores))
#
# scores = run(7999, 13)
# print(get_highest_score(scores))
#
# scores = run(1104, 17)
# print(get_highest_score(scores))

# scores = run(6111, 21)
# print(get_highest_score(scores))

# scores = run(5807, 30)
# print(get_highest_score(scores))

# scores = run(71032, 441)
# print(get_highest_score(scores))

scores = run(7103200, 441)
print(get_highest_score(scores))
