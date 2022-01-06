from collections import deque
from dataclasses import dataclass
from typing import Tuple
from enum import Enum

@dataclass
class TargetArea:
    x1: int
    x2: int
    y1: int
    y2: int


class Status(Enum):
    UNCERTAIN = 0
    HIT = 1
    UNDERSHOT = -1
    OVERSHOT = -2


@dataclass(frozen=True)
class Velocity:
    x: int
    y: int


@dataclass
class Position:
    x: int
    y: int

    def within_target_area(self, target_area) -> Status:
        if (target_area.x1 <= self.x <= target_area.x2) and (target_area.y1 <= self.y <= target_area.y2):
            return Status.HIT
        if (self.y < target_area.y1) and (self.x >= target_area.x2):
            return Status.UNDERSHOT
        if self.y > target_area.y2:
            return Status.OVERSHOT

        return Status.UNCERTAIN


def step(start_position, start_velocity) -> Tuple[Position, Velocity]:

    end_position = Position(start_position.x + start_velocity.x, start_position.y + start_velocity.y)

    if start_velocity.y < 0:
        end_velocity = Velocity(start_velocity.x + 1, start_velocity.y + 1)
    elif start_velocity.y > 0:
        end_velocity = Velocity(start_velocity.x + 1, start_velocity.y - 1)
    else:
        end_velocity = Velocity(start_velocity.x + 1, start_velocity.y)

    return end_position, end_velocity


class MissedException(Exception):
    status: Status

    def __init__(self, status: Status, *args: object) -> None:
        super().__init__(*args)
        self.status = status


def fire(start_velocity, target_area, num_steps=1000):

    start_position = Position(0, 0)
    highest_position = Position(start_position.x, start_position.y)

    for i in range(1, num_steps + 1):
        start_position, start_velocity = step(start_position, start_velocity)

        if start_position.x < highest_position.x:
            highest_position.x = start_position.x
            highest_position.y = start_position.y

        # print(i, start_position, start_velocity)
        target_status = start_position.within_target_area(target_area)
        if target_status == Status.UNDERSHOT or target_status == Status.OVERSHOT:
            raise MissedException(status=target_status)
        if target_status == Status.HIT:
            return highest_position

        # vertical drop
        if start_velocity.y == 0:
            if start_position.x > target_area.x2:
                raise MissedException(status=Status.UNDERSHOT)
            if start_position.y < target_area.y1:
                raise MissedException(status=Status.UNDERSHOT)
            elif start_position.y > target_area.y2:
                raise MissedException(status=Status.OVERSHOT)

    raise Exception('ran out of steps!')


# transposed x=20..30, y=-10..-5
# target_area = TargetArea(5, 10, 20, 30)

# transposed x=94..151, y=-156..-103
target_area = TargetArea(103, 156, 94, 151)



def find_highest_velocity(candidate_start_velocities, target_area, num_steps=1000):
    highest_position = None
    for start_velocity in candidate_start_velocities:
        this_highest_position = fire(start_velocity, target_area, num_steps)
        if not highest_position:
            highest_position = this_highest_position
        elif this_highest_position:
            if this_highest_position.x < highest_position.x:
                highest_position.x = this_highest_position.x
                highest_position.y = this_highest_position.y

    return highest_position


y = target_area.y1

# maximum vertical velocity (quite an assumption and hack)
# max_x = -20
max_x = -250

highest_position = None
start_velocity = Velocity(max_x, 1)

candidate_velocities = deque([start_velocity])

MAX_TRIES = 100000
num_tries = 0  # hacky!

met_criteria = []
already_tried = set()
while candidate_velocities and num_tries < MAX_TRIES:
    candidate_velocity = candidate_velocities.popleft()
    num_tries += 1
    try:
        if candidate_velocity not in already_tried:
            # print('trying velocity = {}'.format(candidate_velocity))
            already_tried.add(candidate_velocity)
            new_highest_position = fire(candidate_velocity, target_area)
            met_criteria.append(candidate_velocity)

            # try more velocities
            candidate_velocities.append(Velocity(candidate_velocity.x, candidate_velocity.y + 1))
            candidate_velocities.append(Velocity(candidate_velocity.x - 1, candidate_velocity.y + 1))
            candidate_velocities.append(Velocity(candidate_velocity.x + 1, candidate_velocity.y + 1))
            candidate_velocities.append(Velocity(candidate_velocity.x, candidate_velocity.y - 1))
            candidate_velocities.append(Velocity(candidate_velocity.x - 1, candidate_velocity.y - 1))
            candidate_velocities.append(Velocity(candidate_velocity.x + 1, candidate_velocity.y - 1))

            # if not highest_position:
            #     highest_position = new_highest_position
            # if new_highest_position.x < highest_position.x:
            #     highest_position.x = new_highest_position.x
            #     highest_position.y = new_highest_position.y
            #     print('found new highest = {}, at velocity = {}'.format(new_highest_position, candidate_velocity))
    except MissedException as e:
        if e.status == Status.UNDERSHOT:  # undershot
            # print('undershot')
            candidate_velocities.append(Velocity(candidate_velocity.x, candidate_velocity.y + 1))
        if e.status == Status.OVERSHOT:  # overshot
            # print('overshot')
            candidate_velocities.append(Velocity(candidate_velocity.x, candidate_velocity.y - 1))
            candidate_velocities.append(Velocity(candidate_velocity.x + 1, candidate_velocity.y))


print(len(met_criteria))
