from pdb import run


def init_array(initial_state, padding):
    return "." * padding + initial_state + "." * padding


def read_into_lookup(filename):
    lookup = {}
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip()
            splits = line.split(" => ")
            lookup[splits[0]] = splits[1]
    return lookup


def run_many_generations(pots, lookup, num_generations=20):
    # iterate through all pots
    for n in range(1, num_generations + 1):
        next_gen_pots = ".."
        for i in range(2, len(pots) - 2):
            signature = pots[i - 2 : i] + pots[i] + pots[i + 1 : i + 3]
            next_gen_value = lookup.get(signature, ".")
            # print(signature, " => ", next_gen_value)
            next_gen_pots += next_gen_value

        print(pots)
        pots = next_gen_pots + ".."

    return pots


def add_pot_numbers_with_plant(pots, padding):
    total = 0
    for i, c in enumerate(pots):
        if c == "#":
            total += i - padding
            print(i, i - padding)
    return total


# initial_state = "#..#.#..##......###...###"
# initial_state = "##..#..##.#....##.#..#.#.##.#.#.######..##.#.#.####.#..#...##...#....#....#.##.###..#..###...#...#.."
# padding = 2000
# pots = init_array(initial_state, padding)
# print(len(pots))
#
# lookup = read_into_lookup("input.txt")

# num_generations = 1100
# pots = run_many_generations(pots, lookup, num_generations)
# print(pots)

# print(add_pot_numbers_with_plant(pots, padding))

# the pots become stable after a few generations.
# in this case, i observed that at 1000 generations, the pots were stable, and the following was the pattern
# this pattern was repeated every next generation, but shifted to the right by one
stable_pots = "#......#....#........#....#....#....#....#........#....#........#....#.....#..........#....#....#....#....#....#....#....#....#..........#........#....#....#........#....#....#....#..#......#....#"
total = 0
offset = 902 + (50000000000 - 1000)
for i, c in enumerate(stable_pots):
    if c == "#":
        total += i + offset
print(total)
