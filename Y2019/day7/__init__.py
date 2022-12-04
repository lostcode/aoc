from Y2019.day5 import Intcode, read_from_file
from threading import Thread
from itertools import cycle


def run_phases(instructions, phases):
    input_signal = None
    for index, phase in enumerate(phases):
        if index == 0:
            input_signal = 0
        inputs = [phase, input_signal]
        computer = Intcode(instructions=instructions)
        computer.supply_many(inputs)
        computer.run()
        output = computer.output
        input_signal = output
    return output


def run_feedback_loop(instructions, phases):
    inputs = [phases[0], 0]
    amp_a = Intcode(instructions, inputs)
    a = Thread(target=amp_a.run())
    a.run()
    inputs = [phases[1]]
    amp_b = Intcode(instructions, inputs)
    b = Thread(target=amp_b.run())
    b.run()
    inputs = [phases[2]]
    amp_c = Intcode(instructions, inputs)
    c = Thread(target=amp_c.run())
    c.run()
    inputs = [phases[3]]
    amp_d = Intcode(instructions, inputs)
    d = Thread(target=amp_d.run())
    d.run()
    inputs = [phases[4]]
    amp_e = Intcode(instructions, inputs)
    e = Thread(target=amp_e.run())
    e.run()

    amps = [amp_a, amp_b, amp_c, amp_d, amp_e]
    index = 0
    prev_output = 0

    while True:
        amps[index].supply_one(prev_output)
        prev_output = amps[index].output.get(block=True)
        index += 1


# fmt: off
instructions = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26, 27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
# fmt: on
phases = [9, 8, 7, 6, 5]
# run_feedback_loop(instructions, phases)


def run_tests():
    instructions = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
    phases = [4, 3, 2, 1, 0]
    assert run_phases(instructions, phases) == 43210

    instructions = [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0]
    phases = [0, 1, 2, 3, 4]
    assert run_phases(instructions, phases) == 54321

    # fmt: off
    instructions = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33, 1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]  # noqa
    # fmt: on
    phases = [1, 0, 4, 3, 2]
    assert run_phases(instructions, phases) == 65210


run_tests()


def get_phase_permutations():
    from itertools import permutations

    return list(permutations([0, 1, 2, 3, 4], 5))


def run_loopless():
    # part A
    instructions = read_from_file("input.txt")
    max_output = 0
    all_outputs = []
    for phases in get_phase_permutations():
        output = run_phases(instructions, phases)
        all_outputs.append(output)
        max_output = max(output, max_output)

    print("max = ", max_output)
    print("all = ", all_outputs)
