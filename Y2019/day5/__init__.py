from queue import Queue


def read_from_file(filename):
    with open(filename, "r") as f:
        return list(map(int, f.read().strip().split(",")))


def parse_opcode(instruction):
    opcode = instruction % 100
    mode_param1 = (instruction // 100) % 10
    mode_param2 = (instruction // 1000) % 10
    mode_param3 = (instruction // 10000) % 10
    return opcode, mode_param1, mode_param2, mode_param3


def fetch_one_param(instructions, position, mode, move_pointer=True):
    immediate_param = instructions[position]
    if mode == 0:
        param = instructions[immediate_param]
        print("fetch positional instructions[{}] -> {}".format(immediate_param, param))
    else:
        print("fetch immediate -> {}".format(immediate_param))
        param = immediate_param

    if move_pointer:
        position += 1
    return param, position


class Intcode:
    def __init__(self, instructions, inputs=None) -> None:
        self.instructions = instructions
        self.inputs = Queue()
        if inputs is not None:
            self.supply_many(inputs)
        self.output = Queue()

    def supply_one(self, inp):
        self.inputs.put(inp)

    def supply_many(self, inps):
        for inp in inps:
            self.inputs.put(inp)

    def run(self):
        position = 0
        output = None
        while True:
            opcode, mode_p1, mode_p2, mode_p3 = parse_opcode(self.instructions[position])
            print(self.instructions[position], position, opcode, mode_p1, mode_p2, mode_p3)
            position += 1
            match opcode:
                case 1:
                    assert mode_p3 != 1
                    param_1, position = fetch_one_param(self.instructions, position, mode_p1)
                    param_2, position = fetch_one_param(self.instructions, position, mode_p2)
                    result_position = self.instructions[position]
                    self.instructions[result_position] = param_1 + param_2
                    print("OP: instr[{}] = {} + {}".format(result_position, param_1, param_2))
                    position += 1
                case 2:
                    assert mode_p3 != 1
                    param_1, position = fetch_one_param(self.instructions, position, mode_p1)
                    param_2, position = fetch_one_param(self.instructions, position, mode_p2)
                    result_position = self.instructions[position]
                    self.instructions[result_position] = param_1 * param_2
                    print("OP: instr[{}] = {} x {}".format(result_position, param_1, param_2))
                    position += 1
                case 3:
                    # only one input
                    param, position = fetch_one_param(self.instructions, position, 1)
                    _input = self.inputs.get(block=True)
                    self.instructions[param] = _input
                    print("OP: instr[{}] = {}".format(param, _input))
                case 4:
                    param, position = fetch_one_param(self.instructions, position, 0)
                    self.output.put(param)
                    print("OP: output : ", param)
                case 5:
                    # jump-if-true
                    param_1, position = fetch_one_param(self.instructions, position, mode_p1)
                    if param_1:
                        param_2, _ = fetch_one_param(self.instructions, position, mode_p2, move_pointer=False)
                        position = param_2
                        print("OP: GOTO {}".format(position))
                    else:
                        position += 1
                case 6:
                    # jump-if-false
                    param_1, position = fetch_one_param(self.instructions, position, mode_p1)
                    if not param_1:
                        param_2, _ = fetch_one_param(self.instructions, position, mode_p2, move_pointer=False)
                        position = param_2
                        print("OP: GOTO {}".format(position))
                    else:
                        position += 1
                case 7:
                    param_1, position = fetch_one_param(self.instructions, position, mode_p1)
                    param_2, position = fetch_one_param(self.instructions, position, mode_p2)
                    param_3 = self.instructions[position]
                    position += 1
                    if param_1 < param_2:
                        self.instructions[param_3] = 1
                        print("OP: {} < {}, instr[{}] = 1".format(param_1, param_2, param_3))
                    else:
                        self.instructions[param_3] = 0
                        print("OP: {} >= {}, instr[{}] = 0".format(param_1, param_2, param_3))
                case 8:
                    param_1, position = fetch_one_param(self.instructions, position, mode_p1)
                    param_2, position = fetch_one_param(self.instructions, position, mode_p2)
                    param_3 = self.instructions[position]
                    position += 1
                    if param_1 == param_2:
                        self.instructions[param_3] = 1
                        print("OP: {} == {}, instr[{}] = 1".format(param_1, param_2, param_3))
                    else:
                        self.instructions[param_3] = 0
                        print("OP: {} != {}, instr[{}] = 0".format(param_1, param_2, param_3))
                case 99:
                    return


# run([3, 0, 4, 0, 99], [10000])
# print(run([1002, 4, 3, 4, 33], []))
# print(run([1101, 100, -1, 4, 0], []))
# instructions, output = run(read_from_file("input.txt"), [5])
# print("output = ", output)
# print(run([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [0]))
# print(run([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [9]))
# print(run([3, 3, 1107, -1, 8, 3, 4, 3, 99], [9]))
