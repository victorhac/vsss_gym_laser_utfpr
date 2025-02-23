from lib.curriculum.behaviors.behavior import Behavior
from lib.domain.behavior_args import BehaviorArgs
from lib.domain.enums.role_enum import RoleEnum
from lib.supporter.default_supporter import get_supporter_speeds
from lib.utils.model_utils import ModelUtils
from lib.utils.roles.role_utils import RoleUtils

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
            left_speed, right_speed = self._get_from_model_speeds(
                environment,
                args
            )

        return self._get_final_speeds(left_speed, right_speed)
    
    def _get_supporter_speeds(
        self,
        environment
    ):
        field = environment.opponent_field if self.is_yellow else environment.field
        return get_supporter_speeds(
            self.robot_id,
            field
        )
    
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
