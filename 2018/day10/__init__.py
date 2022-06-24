import numpy as np
import sys
from io import StringIO

with open("input.txt", "r") as f:
    data = f.read()

# read into a series of [x, y, dx, dy] values
stars = np.fromregex(
    StringIO(data),
    r"position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>",
    [("x", np.int32), ("y", np.int32), ("dx", np.int32), ("dy", np.int32)],
)


def print_image(stars):
    max_x = stars["x"].max() + 1
    max_y = stars["y"].max() + 1

    image = np.full((max_x, max_y), False)
    for star in stars:
        image[star[0], star[1]] = True

    image = np.transpose(image)
    np.set_printoptions(threshold=sys.maxsize, linewidth=100000)
    print(np.array2string(image, separator="", formatter={"bool": " #".__getitem__}))


def move_one_step(stars, direction=1):
    stars["x"] += stars["dx"] * direction
    stars["y"] += stars["dy"] * direction


# move enough steps to converge to the minimum "spread" between the y points
def move_the_right_steps(stars) -> int:
    num_steps = 0
    max_y, min_y = stars["y"].max(), stars["y"].min()
    diff_y = max_y - min_y
    while True:
        move_one_step(stars)
        num_steps += 1
        max_y, min_y = stars["y"].max(), stars["y"].min()
        new_diff_y = max_y - min_y
        if new_diff_y > diff_y:
            break
        diff_y = new_diff_y

    # move one back because we went over
    move_one_step(stars, -1)
    num_steps -= 1

    return num_steps


num_steps = move_the_right_steps(stars)

print_image(stars)
print("num steps = ", num_steps)
