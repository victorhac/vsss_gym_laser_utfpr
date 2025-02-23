from lib.domain.robot import Robot
from lib.domain.ball import Ball

class Field:
    def __init__(self):
        self._robots = {
            0: Robot(0, False),
            1: Robot(1, False),
            2: Robot(2, False)
        }
        self._foes = {
            0: Robot(0, False),
            1: Robot(1, False),
            2: Robot(2, False)
        }
        self.ball = Ball()

    def get_robot_by_id(self, id: int):
        return self._robots[id]
    
    def get_foe_by_id(self, id: int):
        return self._foes[id]
    
    def set_robots(self, robots: 'dict[int, Robot]'):
        self._robots = robots
    
    def set_foes(self, foes: 'dict[int, Robot]'):
        self._foes = foes

    def get_active_robots(self) -> 'list[float]':
        robots = []

        for i in range(3):
            robot = self._robots[i]
            if robot.active:
                robots.append(robot)

        return robots

    def get_active_foes(self) -> 'list[float]':
        robots = []

        for i in range(3):
            robot = self._foes[i]
            if robot.active:
                robots.append(robot)

        return robots

    def __str__(self):
        msg = f'BALL\n{self.ball}'
        for i in range(3):
            robot = self._robots[i]
            if robot is not None:
                msg += f'\nROBOT_{i}\n{robot}'
        for i in range(3):
            robot = self._foes[i]
            if robot is not None:
                msg += f'\nFOE_{i}\n{robot}'
        return msg

    def __repr__(self):
        return f'FieldData({self})'