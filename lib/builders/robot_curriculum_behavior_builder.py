from lib.domain.robot_curriculum_behavior import RobotCurriculumBehavior
from lib.domain.enums.position_enum import PositionEnum
from lib.domain.enums.robot_curriculum_behavior_enum import RobotCurriculumBehaviorEnum

class RobotCurriculumBehaviorBuilder:
    def __init__(
        self,
        robot_id: int,
        is_yellow: bool,
        updates_per_task: int
    ):
        self.robot_id = robot_id
        self.is_yellow = is_yellow
        self.updates_per_task = updates_per_task

        self.position_enum = None
        self.distance_range = None
        self.velocity_alpha_range = None
        self.model_path = None

    def set_ball_following_behavior(self):
        self.robot_curriculum_behavior_enum = RobotCurriculumBehaviorEnum.BALL_FOLLOWING
        return self
    
    def set_goalkeeper_ball_following_behavior(self):
        self.robot_curriculum_behavior_enum = RobotCurriculumBehaviorEnum.GOALKEEPER_BALL_FOLLOWING
        return self
    
    def set_from_previous_model_behavior(self, model_path: 'str | None' = None):
        self.robot_curriculum_behavior_enum = RobotCurriculumBehaviorEnum.FROM_PREVIOUS_MODEL
        self.model_path = model_path
        return self
    
    def set_from_fixed_model_behavior(self, model_path: str):
        self.robot_curriculum_behavior_enum = RobotCurriculumBehaviorEnum.FROM_FIXED_MODEL
        self.model_path = model_path
        return self
    
    def set_from_model_behavior(self):
        self.robot_curriculum_behavior_enum = RobotCurriculumBehaviorEnum.FROM_MODEL
        return self

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

        if self.model_path is not None:
            robot_curriculum_behavior.set_model_path(self.model_path)
            
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