from lib.curriculum.behaviors.ball_following_behavior import BallFollowingBehavior
from lib.curriculum.behaviors.from_fixed_model_behavior import FromFixedModelBehavior
from lib.curriculum.behaviors.from_model_behavior import FromModelBehavior
from lib.curriculum.behaviors.from_previous_model_behavior import FromPreviousModelBehavior
from lib.curriculum.behaviors.goalkeeper_ball_following_behavior import GoalkeeperBallFollowingBehavior
from lib.curriculum.behaviors.multiple_role_behavior import MultipleRoleBehavior
from lib.domain.enums.role_enum import RoleEnum
from lib.curriculum.robot_curriculum_behavior import RobotCurriculumBehavior
from lib.curriculum.position_setup.position_setup import PositionSetup

class RobotCurriculumBehaviorBuilder:
    def __init__(
        self,
        robot_id: int,
        is_yellow: bool,
        updates_per_task: int,
        position_setup: PositionSetup
    ):
        self.robot_id = robot_id
        self.is_yellow = is_yellow
        self.updates_per_task = updates_per_task

        self.position_setup = position_setup
        self.distance_range = None
        self.velocity_alpha_range = None

    def set_ball_following_behavior(self):
        self.behavior = BallFollowingBehavior(
            self.robot_id,
            self.is_yellow
        )
        return self
    
    def set_goalkeeper_ball_following_behavior(self):
        self.behavior = GoalkeeperBallFollowingBehavior(
            self.robot_id,
            self.is_yellow
        )
        return self
    
    def set_from_previous_model_behavior(
        self,
        role_enum: RoleEnum,
        deterministic: bool = True
    ):
        self.behavior = FromPreviousModelBehavior(
            self.robot_id,
            self.is_yellow,
            role_enum,
            deterministic
        )
        return self
    
    def set_from_fixed_model_behavior(
        self,
        model_path: str,
        role_enum: RoleEnum = RoleEnum.ATTACKER,
        deterministic: bool = True
    ):
        self.behavior = FromFixedModelBehavior(
            self.robot_id,
            self.is_yellow,
            role_enum,
            model_path,
            deterministic
        )
        return self
    
    def set_from_model_behavior(self):
        self.behavior = FromModelBehavior(
            self.robot_id,
            self.is_yellow
        )
        return self
    
    def set_multiple_role_behavior(
        self,
        deterministic: bool = True
    ):
        self.behavior = MultipleRoleBehavior(
            self.robot_id,
            self.is_yellow,
            deterministic
        )
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
            self.behavior,
            self.position_setup,
            self.updates_per_task
        )
        
        if self.distance_range is not None:
            self._set_distance_range(robot_curriculum_behavior)

        if self.velocity_alpha_range is not None:
            self._set_velocity_alpha_range(robot_curriculum_behavior)
            
        return robot_curriculum_behavior
    
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