import copy


class Cart:
    def __init__(self, i, j, direction) -> None:
        self.i = i
        self.j = j
        self.direction = direction
        self.next_turn = -1

    def next_turn_at_intersection(self):
        self.next_turn = (self.next_turn + 1) % 3
        return self.next_turn

    def move_one_step(self, paths):
        on_path = paths[self.i][self.j]
        if self.direction == ">":
            if on_path == "/":
                self.j += 1
            elif on_path == "\\":
                self.j += 1
            elif on_path == "-":
                self.j += 1
            elif on_path == "+":
                next_turn = self.next_turn_at_intersection()
                if next_turn == 0:
                    self.i -= 1
                    self.direction = "^"
                elif next_turn == 1:
                    self.j += 1
                    self.direction = ">"
                else:
                    self.i += 1
                    self.direction = "v"

            new_path = paths[self.i][self.j]
            if new_path == "\\":
                self.direction = "v"
            elif new_path == "/":
                self.direction = "^"
            elif new_path == "+":
                next_turn = self.next_turn_at_intersection()
                if next_turn == 0:
                    self.direction = "^"
                elif next_turn == 1:
                    self.direction = ">"
                elif next_turn == 2:
                    self.direction = "v"
                else:
                    raise Exception("unexpected next_turn", next_turn)
            else:
                raise Exception("unexpected on_path = ", on_path)

        elif self.direction == "<":
            if on_path == "/":
                self.j -= 1
            elif on_path == "\\":
                self.j -= 1
            elif on_path in ("-", "+"):
                self.j -= 1
                new_path = paths[self.i][self.j]
                if new_path == "\\":
                    self.direction = "^"
                elif new_path == "/":
                    self.direction = "v"
                elif new_path == "+":
                    next_turn = self.next_turn_at_intersection()
                    if next_turn == 0:
                        self.direction = "v"
                    elif next_turn == 1:
                        self.direction = "<"
                    elif next_turn == 2:
                        self.direction = "^"
                    else:
                        raise Exception("unexpected next_turn", next_turn)
            else:
                raise Exception("unexpected on_path = ", on_path)
        elif self.direction == "v":
            if on_path == "/":
                self.i += 1
            elif on_path == "\\":
                self.i += 1
            elif on_path in ("|", "+"):
                self.i += 1
                new_path = paths[self.i][self.j]
                if new_path == "\\":
                    self.direction = ">"
                elif new_path == "/":
                    self.direction = "<"
                elif new_path == "+":
                    next_turn = self.next_turn_at_intersection()
                    if next_turn == 0:
                        self.direction = ">"
                    elif next_turn == 1:
                        self.direction = "v"
                    elif next_turn == 2:
                        self.direction = "<"
                    else:
                        raise Exception("unexpected next_turn", next_turn)
            else:
                raise Exception("unexpected on_path = ", on_path)
        elif self.direction == "^":
            if on_path == "/":
                self.i -= 1
            elif on_path == "\\":
                self.i -= 1
            elif on_path in ("|", "+"):
                self.i -= 1
                new_path = paths[self.i][self.j]
                if new_path == "\\":
                    self.direction = "<"
                elif new_path == "/":
                    self.direction = ">"
                elif new_path == "+":
                    next_turn = self.next_turn_at_intersection()
                    if next_turn == 0:
                        self.direction = "<"
                    elif next_turn == 1:
                        self.direction = "^"
                    elif next_turn == 2:
                        self.direction = ">"
                    else:
                        raise Exception("unexpected next_turn", next_turn)
            else:
                raise Exception("unexpected on_path = ", on_path)

    def __repr__(self) -> str:
        return "Cart({}, {}, {})".format(self.i, self.j, self.direction)

    def __lt__(self, other):
        return (self.i, self.j) < (other.i, other.j)


def read_map(filename):
    paths = []
    carts = []
    i = 0
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.rstrip()
            replaced_line = ""
            j = 0
            for c in line:
                if c in ("<", ">", "v", "^"):
                    carts.append(Cart(i, j, c))
                    if c in ("<", ">"):
                        replaced_line += "-"
                    else:
                        replaced_line += "|"
                else:
                    replaced_line += c
                j += 1
            paths.append(replaced_line)
            i += 1
    return paths, carts


def overlap_carts_on_paths(carts, paths):
    overlaid_paths = copy.deepcopy(paths)
    carts = sorted(carts)
    for cart in carts:
        line = overlaid_paths[cart.i]
        new_line = line[: cart.j] + cart.direction + line[cart.j + 1 :]
        overlaid_paths[cart.i] = new_line
    return overlaid_paths


paths, carts = read_map("input.txt")


def check_collisions(cart_with_new_position, other_carts):
    for cart in other_carts:
        if cart.i == cart_with_new_position.i and cart.j == cart_with_new_position.j:
            return True
    return False


def tick(carts, paths):
    carts = sorted(carts)
    print(carts)
    for i, cart in enumerate(carts):
        cart.move_one_step(paths)
        if check_collisions(cart, carts[:i] + carts[i + 1 :]):
            raise Exception("Found collision at ", cart.i, cart.j)
    return carts


for path in overlap_carts_on_paths(carts, paths):
    print(path)

for i in range(100):
    tick(carts, paths)
    # carts = sorted(carts)
    # print(carts)
    # for path in overlap_carts_on_paths(carts, paths):
    #     print(path)
    # print()
