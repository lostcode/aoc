def read_from_file(filename):
    with open(filename, "r") as f:
        return list(map(int, f.read().strip().split(",")))


def fetch_two_operands(instructions, position):
    op1_position = instructions[position]
    op1 = instructions[op1_position]
    position += 1
    op2_position = instructions[position]
    op2 = instructions[op2_position]
    position += 1
    return op1, op2, position


def run(instructions):
    position = 0
    while True:
        opcode = instructions[position]
        position += 1
        match opcode:
            case 1:
                op1, op2, position = fetch_two_operands(instructions, position)
                result_position = instructions[position]
                instructions[result_position] = op1 + op2
                position += 1
            case 2:
                op1, op2, position = fetch_two_operands(instructions, position)
                result_position = instructions[position]
                instructions[result_position] = op1 * op2
                position += 1
            case 99:
                break
    return instructions


# instructions = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
# instructions = [1, 1, 1, 4, 99, 5, 6, 0, 99]
instructions = read_from_file("input.txt")
instructions[1] = 12
instructions[2] = 2

print(run(instructions))
