from lib.domain.enums.role_enum import RoleEnum
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
        self.distance_to_wall = None
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
    
    def set_from_fixed_model_behavior(
        self,
        model_path: str,
        role_enum: RoleEnum = RoleEnum.ATTACKER
    ):
        self.robot_curriculum_behavior_enum = RobotCurriculumBehaviorEnum.FROM_FIXED_MODEL
        self.role_enum = role_enum
        self.model_path = model_path
        return self
    
    def set_from_model_behavior(self):
        self.robot_curriculum_behavior_enum = RobotCurriculumBehaviorEnum.FROM_MODEL
        return self
    
    def set_multiple_role_behavior(self):
        self.robot_curriculum_behavior_enum = RobotCurriculumBehaviorEnum.MULTIPLE_ROLE
        return self

    def set_position_enum(
        self,
        position_enum: PositionEnum
    ):
        self.position_enum = position_enum
        return self
    
    def set_own_goal_relative_to_wall_position_enum(
        self,
        distance_to_wall: float
    ):
        self.distance_to_wall = distance_to_wall
        self.position_enum = PositionEnum.OWN_GOAL_RELATIVE_TO_WALL
        return self
    
    def set_opponent_goal_relative_to_wall_position_enum(
        self,
        distance_to_wall: float
    ):
        self.distance_to_wall = distance_to_wall
        self.position_enum = PositionEnum.OPPONENT_GOAL_RELATIVE_TO_WALL
        return self
    
    def set_relative_to_own_vertical_line_position_enum(
        self,
        x_line: float,
        y_range: 'tuple[float, float]',
        left_to_line: bool
    ):
        self.x_line = x_line
        self.y_range = y_range
        self.left_to_line = left_to_line
        self.position_enum = PositionEnum.RELATIVE_TO_OWN_VERTICAL_LINE
        return self
    
    def set_relative_to_opponent_vertical_line_position_enum(
        self,
        x_line: float,
        y_range: 'tuple[float, float]',
        left_to_line: bool
    ):
        self.x_line = x_line
        self.y_range = y_range
        self.left_to_line = left_to_line
        self.position_enum = PositionEnum.RELATIVE_TO_OPPONENT_VERTICAL_LINE
        return self
    
    def set_fixed_position_enum(
        self,
        position: 'tuple[float, float]'
    ):
        self.fixed_position = position
        self.position_enum = PositionEnum.FIXED
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
            robot_curriculum_behavior.set_model_path(
                self.model_path,
                self.role_enum
            )
            
        return robot_curriculum_behavior

    def _set_position_enum(
        self,
        robot_curriculum_behavior: RobotCurriculumBehavior
    ):
        robot_curriculum_behavior.position_enum = self.position_enum

        if self.position_enum == PositionEnum.OWN_GOAL_RELATIVE_TO_WALL or\
                self.position_enum == PositionEnum.OPPONENT_GOAL_RELATIVE_TO_WALL:
            robot_curriculum_behavior.set_distance_to_wall(self.distance_to_wall)
        elif self.position_enum == PositionEnum.RELATIVE_TO_OWN_VERTICAL_LINE or\
                self.position_enum == PositionEnum.RELATIVE_TO_OPPONENT_VERTICAL_LINE:
            robot_curriculum_behavior.set_relative_to_vertical_line_position_enum_values(
                self.x_line,
                self.y_range,
                self.left_to_line)
        elif self.position_enum == PositionEnum.FIXED:
            robot_curriculum_behavior.set_fixed_position(self.fixed_position)
    
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