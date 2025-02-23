import numpy as np

from lib.curriculum.behaviors.behavior import Behavior
from lib.curriculum.position_setup.position_setup import PositionSetup

class RobotCurriculumBehavior:
    def __init__(
        self,
        robot_id: int,
        is_yellow: bool,
        behavior: Behavior,
        position_setup: PositionSetup,
        updates_per_task: int
    ):
        self.robot_id = robot_id
        self.is_yellow = is_yellow
        self.updates_per_task = updates_per_task
        self.behavior = behavior

        self.updates = 0

        self.distance = None
        self.distance_range = None
        self.distance_beta = None

        self.velocity_alpha = None
        self.velocity_alpha_range = None
        self.velocity_beta = None

        self.position_setup = position_setup

    def set_distance_range(
        self,
        distance_range: 'tuple[float, float]'
    ):
        self.distance_range = distance_range
        self._try_set_distance()
    
    def set_velocity_alpha_range(
        self,
        velocity_alpha_range: 'tuple[float, float]'
    ):
        self.velocity_alpha_range = velocity_alpha_range
        self._try_set_velocity_alpha()

    def _try_set_distance(self):
        if self.distance_range is not None:
            self.distance = self.distance_range[0]
            
            self.distance_beta = RobotCurriculumBehavior._get_beta(
                self.distance_range,
                self.updates_per_task)
            
    def _try_set_velocity_alpha(self):
        if self.velocity_alpha_range is not None:
            self.velocity_alpha = self.velocity_alpha_range[0]

            self.velocity_beta = RobotCurriculumBehavior._get_beta(
                self.velocity_alpha_range,
                self.updates_per_task)

    def update(self, times: int = 1):
        def clip(value: float, range: 'tuple[float, float]'):
            if range[0] > range[1]:
                return np.clip(value, range[1], range[0])
            
            return np.clip(value, range[0], range[1])
        
        if self.distance_range is not None:
            self.distance = clip(
                self.distance + self.distance_beta * times,
                self.distance_range)
            
        if self.velocity_alpha_range is not None:
            self.velocity_alpha = clip(
                self.velocity_alpha + self.velocity_beta * times,
                self.velocity_alpha_range)
            
            self.behavior.velocity_alpha = self.velocity_alpha
            
        self.updates = clip(self.updates + times, (0, 100))

    def reset(self):
        if self.velocity_alpha_range is not None:
            self.velocity_alpha = self.velocity_alpha_range[0]
            self.behavior.velocity_alpha = self.velocity_alpha
        else:
            self.velocity_alpha = None

        if self.distance_range is not None:
            self.distance = self.distance_range[0]
        else:
            self.distance = None

        self.behavior.reset()
        self.updates = 0

    def is_over(self):
        return self.updates == self.updates_per_task
    
    def get_velocity_alpha(self):
        if self.velocity_alpha_range is None:
            return 1
        return self.velocity_alpha
    
    @staticmethod
    def _get_beta(
        range: 'tuple[float, float]',
        updates_per_task: int
    ):
        return (range[1] - range[0]) / updates_per_task