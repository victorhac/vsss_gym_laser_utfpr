from lib.behaviors.behavior import Behavior
from lib.behaviors.behavior_args import BehaviorArgs
from lib.domain.enums.role_enum import RoleEnum
from lib.utils.model_utils import ModelUtils
from lib.utils.roles.role_utils import RoleUtils

class FromFixedModelBehavior(Behavior):
    def __init__(
        self,
        robot_id: int,
        is_yellow: bool,
        role_enum: RoleEnum,
        model_path = str,
        deterministic: bool = False
    ):
        super().__init__(
            robot_id,
            is_yellow
        )

        self.role_enum = role_enum
        self.model_id = ModelUtils.get_id()
        self.model = ModelUtils.get_model(self.model_id, model_path)
        self.deterministic = deterministic

    def get_speeds(
        self,
        environment,
        args: 'BehaviorArgs | None' = None
    ):
        left_speed, right_speed = RoleUtils.get_speeds(
            environment,
            self.role_enum,
            self.robot_id,
            self.is_yellow,
            not self.is_yellow,
            self.model,
            self.deterministic
        )

        return self._get_final_speeds(left_speed, right_speed)
