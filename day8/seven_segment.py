from typing import List
from dataclasses import dataclass


class Sex(Enum):
    FEMALE = 0
    MALE = 1

class Relationship(Enum):
    PARENT = 0
    SIBLING = 1


@dataclass
class RelativeDiseaseStatus:
    label: str   # eg. “Cardiac Ischemia”, or “Coronary Heart Disease”
    relationship: Relationship
    sex: Sex
    age_of_onset: int


@dataclass
class Reading:
    signals: List
    digits: List


def read_input(filename):
    readings = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            signals = line.strip().split(' | ')[0].split(' ')
            digits = line.strip().split(' | ')[1].split(' ')
            readings.append(Reading(signals, digits))
    return readings


readings = read_input('easy_short_input.txt')

# times = 0
# for reading in readings:
#     for digit in reading.digits:
#         if len(digit) in {2, 3, 4, 7}:
#             times += 1
#
# print(times)

WIRES = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}
SEGMENTS = {0, 1, 2, 3, 4, 5, 6}

wire_to_segment = {wire: SEGMENTS for wire in WIRES}

# for reading in readings:  # TODO
for signal in readings[0].signals:
    if len(signal) == 2:  # digit: 1
        for wire in signal:
            wire_to_segment[wire] = {2, 5}
        for wire in WIRES - set(signal):
            wire_to_segment[wire] -= {2, 5}



print(wire_to_segment)

