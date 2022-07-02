def run(after):
    arr = [3, 7]
    i = 0
    j = 1

    while True:
        i = (i + arr[i] + 1) % len(arr)
        j = (j + arr[j] + 1) % len(arr)

        added = arr[i] + arr[j]
        digits = [int(c) for c in str(added)]
        arr.extend(digits)

        if len(arr) >= after + 10:
            return arr[after : after + 10]


def run_before(before_sequence):
    arr = [3, 7]
    i = 0
    j = 1
    last_window_start = 0

    while True:
        i = (i + arr[i] + 1) % len(arr)
        j = (j + arr[j] + 1) % len(arr)

        added = arr[i] + arr[j]
        digits = [int(c) for c in str(added)]
        arr.extend(digits)

        while last_window_start < len(arr) - len(before_sequence):
            # print(arr[k : k + len(before_sequence)])
            if (
                arr[last_window_start : last_window_start + len(before_sequence)]
                == before_sequence
            ):
                return last_window_start
            last_window_start += 1


# next_10 = run(after=170641)
# print("".join(str(c) for c in next_10))

# before_i = run_before(before_sequence=[5, 1, 5, 8, 9])
# before_i = run_before(before_sequence=[5, 9, 4, 1, 4])
before_i = run_before(before_sequence=[1, 7, 0, 6, 4, 1])
print(before_i)
