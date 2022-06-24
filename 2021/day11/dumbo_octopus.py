import numpy as np
from scipy.signal import convolve2d

octopuses = np.genfromtxt("""
2682551651
3223134263
5848471412
7438334862
8731321573
6415233574
5564726843
6683456445
8582346112
4617588236
""".splitlines(), dtype=np.uint8, delimiter=1)

KERNEL = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=np.uint8)


def step(octopuses):
    octopuses += 1
    num_flashed = 0
    flashed = np.zeros(octopuses.shape, dtype=np.bool_)
    while True:
        flashing = ~flashed & (octopuses > 9)
        if not np.any(flashing):
            break

        energies = convolve2d(flashing, KERNEL, mode="same")
        flashed = octopuses > 9

        octopuses += energies

    num_flashed += np.sum(flashed)
    octopuses[octopuses > 9] = 0

    return octopuses, num_flashed


total_flashes = 0
num_steps = 1
while True:
    octopuses, num_flashed = step(octopuses)
    if num_flashed == 100:
        print('all flashed at step: ', num_steps)
        break
    num_steps += 1
