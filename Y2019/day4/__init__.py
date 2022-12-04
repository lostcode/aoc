from collections import Counter


def is_valid(password):
    prev_digit = password // 10**5
    counter = Counter({prev_digit: 1})
    max_digit = prev_digit
    for i in range(1, 6):
        current_digit = (password // 10 ** (5 - i)) % 10
        counter[current_digit] += 1
        if current_digit < max_digit:
            return False
        max_digit = max(max_digit, current_digit)
    for digit, times in counter.items():
        if times == 2:
            return True
    return False


assert not is_valid(111111)
assert not is_valid(223450)
assert not is_valid(123789)
assert not is_valid(799878)
assert is_valid(278899)

assert is_valid(112233)
assert not is_valid(123444)
assert is_valid(111122)

num_valid = 0
for password in range(278384, 824796):
    if is_valid(password):
        num_valid += 1

print(num_valid)
