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
        self.robot_curriculum_behavior = RobotCurriculumBehavior(
            robot_id,
            is_yellow,
            robot_curriculum_behavior_enum,
            updates_per_task
        )

    def set_position_enum(
        self,
        position_enum: PositionEnum
    ):
        self.robot_curriculum_behavior.position_enum = position_enum
        return self
    
    def set_distance_range(
        self,
        distance_range: 'tuple[float, float]',
        is_positive_distance_beta: bool
    ):
        self.robot_curriculum_behavior.set_distance_range(
            distance_range,
            is_positive_distance_beta)

        return self
    
    def set_velocity_alpha_range(
        self,
        velocity_alpha_range,
        is_positive_velocity_beta
    ):
        self.robot_curriculum_behavior.set_velocity_alpha_range(
            velocity_alpha_range,
            is_positive_velocity_beta)

        return self
    
    def build(self):
        return self.robot_curriculum_behavior