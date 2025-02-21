from lib.behaviors.behavior import Behavior
from lib.behaviors.behavior_args import BehaviorArgs
from lib.domain.enums.role_enum import RoleEnum
from lib.positioning.default_supporter_positioning import get_supporter_position
from lib.utils.field_utils import FieldUtils
from lib.utils.model_utils import ModelUtils
from lib.utils.motion_utils import MotionUtils
from lib.utils.roles.role_utils import RoleUtils
from lib.utils.rsoccer.rsoccer_utils import RSoccerUtils

class MultipleRoleBehavior(Behavior):
    def __init__(
        self,
        robot_id: int,
        is_yellow: bool,
        deterministic: bool = True
    ):
        super().__init__(
            robot_id,
            is_yellow
        )

        self.deterministic = deterministic

    def get_speeds(
        self,
        environment,
        args: BehaviorArgs
    ):
        if args.role_enum == RoleEnum.SUPPORTER:
            left_speed, right_speed = self._get_supporter_speeds(environment)
        else:
            left_speed, right_speed = self._get_from_model_speeds(environment, args)

        return self._get_final_speeds(left_speed, right_speed)
    
    def _get_supporter_speeds(self, environment):
        field = RSoccerUtils.get_field_by_frame(environment.frame, self.is_yellow)

        robot = field.get_robot_by_id(self.robot_id)

        obstacles = FieldUtils.to_obstacles_except_current_robot_and_ball(
            field,
            self.robot_id)

        position = get_supporter_position(
            self.robot_id,
            field)

        right_speed, left_speed = MotionUtils.go_to_point_univector(
            robot,
            position,
            obstacles)
        
        return right_speed, left_speed
    
    def _get_from_model_speeds(
        self,
        environment,
        args: BehaviorArgs
    ):
        model = ModelUtils.get_model_by_role_enum(args.role_enum)

        if model is None:
            return 0, 0
        
        left_speed, right_speed = RoleUtils.get_speeds(
            environment,
            args.role_enum,
            self.robot_id,
            self.is_yellow,
            not self.is_yellow,
            model,
            self.deterministic
        )

        return self._get_final_speeds(left_speed, right_speed)
