from lib.domain.enums.robot_curriculum_behavior_enum import RobotCurriculumBehaviorEnum
import numpy as np

from lib.domain.enums.role_enum import RoleEnum

class RobotCurriculumBehavior:
    def __init__(
        self,
        robot_id: int,
        is_yellow: bool,
        robot_curriculum_behavior_enum: RobotCurriculumBehaviorEnum,
        updates_per_task: int
    ):
        self.robot_id = robot_id
        self.is_yellow = is_yellow
        self.robot_curriculum_behavior_enum = robot_curriculum_behavior_enum
        self.updates_per_task = updates_per_task

        self.updates = 0

        self.position_enum = None

        self.distance = None
        self.distance_range = None
        self.distance_beta = None
        self.distance_to_wall = None

        self.velocity_alpha = None
        self.velocity_alpha_range = None
        self.velocity_beta = None

        self.x_line = None
        self.y_range = None
        self.left_to_line = None

        self.fixed_position = None

        self.model_path = None

    def set_distance_to_wall(
        self,
        distance_to_wall: float
    ):
        self.distance_to_wall = distance_to_wall

    def set_fixed_position(
        self,
        position: 'tuple[float, float]'
    ):
        self.fixed_position = position

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

    def set_model_path(
        self,
        model_path: str,
        role_enum: RoleEnum = RoleEnum.ATTACKER
    ):
        self.model_path = model_path
        self.role_enum = role_enum

    def set_relative_to_vertical_line_position_enum_values(
        self,
        x_line: float,
        y_range: 'tuple[float, float]',
        left_to_line: bool
    ):
        self.x_line = x_line
        self.y_range = y_range
        self.left_to_line = left_to_line

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
            
        self.updates = clip(self.updates + times, (0, 100))

    def reset(self):
        if self.velocity_alpha_range is not None:
            self.velocity_alpha = self.velocity_alpha_range[0]
        else:
            self.velocity_alpha = None

        if self.distance_range is not None:
            self.distance = self.distance_range[0]
        else:
            self.distance = None

        self.model_path = None
        self.updates = 0
        
    def _is_distance_in_limit(self):
        if self.distance_range is None:
            return True
        
        return self.distance == self.distance_range[1]
    
    def _is_velocity_alpha_in_limit(self):
        if self.velocity_alpha_range is None:
            return True
        
        return self.velocity_alpha == self.velocity_alpha_range[1]

    def is_over(self):
        return self.updates == self.updates_per_task
    
    def has_behavior(
        self,
        robot_curriculum_behavior_enum: RobotCurriculumBehaviorEnum
    ):
        return self.robot_curriculum_behavior_enum == robot_curriculum_behavior_enum
    
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