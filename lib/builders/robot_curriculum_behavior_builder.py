from lib.domain.robot_curriculum_behavior import RobotCurriculumBehavior
from lib.enums.position_enum import PositionEnum
from lib.enums.robot_curriculum_behavior_enum import RobotCurriculumBehaviorEnum

class RobotCurriculumBehaviorBuilder:
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

        self.position_enum = None
        self.distance_range = None
        self.velocity_alpha_range = None

    def set_position_enum(
        self,
        position_enum: PositionEnum
    ):
        self.position_enum = position_enum
        return self
    
    def set_distance_range(
        self,
        distance_range: 'tuple[float, float]'
    ):
        self.distance_range = distance_range
        return self
    
    def set_velocity_alpha_range(
        self,
        velocity_alpha_range: 'tuple[float, float]'
    ):
        self.velocity_alpha_range = velocity_alpha_range
        return self
    
    def build(self):
        robot_curriculum_behavior = RobotCurriculumBehavior(
            self.robot_id,
            self.is_yellow,
            self.robot_curriculum_behavior_enum,
            self.updates_per_task
        )

        if self.position_enum is not None:
            self._set_position_enum(robot_curriculum_behavior)
        
        if self.distance_range is not None:
            self._set_distance_range(robot_curriculum_behavior)

        if self.velocity_alpha_range is not None:
            self._set_velocity_alpha_range(robot_curriculum_behavior)
            
        return robot_curriculum_behavior

    def _set_position_enum(
        self,
        robot_curriculum_behavior: RobotCurriculumBehavior
    ):
        robot_curriculum_behavior.position_enum = self.position_enum
    
    def _set_distance_range(
        self,
        robot_curriculum_behavior: RobotCurriculumBehavior
    ):
        robot_curriculum_behavior.set_distance_range(
            self.distance_range)
    
    def _set_velocity_alpha_range(
        self,
        robot_curriculum_behavior: RobotCurriculumBehavior
    ):
        robot_curriculum_behavior.set_velocity_alpha_range(
            self.velocity_alpha_range)