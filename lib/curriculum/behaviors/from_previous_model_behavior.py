from lib.curriculum.behaviors.behavior import Behavior
from lib.domain.behavior_args import BehaviorArgs
from lib.domain.enums.role_enum import RoleEnum
from lib.utils.model_utils import ModelUtils
from lib.utils.roles.role_utils import RoleUtils

class FromPreviousModelBehavior(Behavior):
    def __init__(
        self,
        robot_id: int,
        is_yellow: bool,
        role_enum: RoleEnum,
        deterministic: bool = False
    ):
        super().__init__(
            robot_id,
            is_yellow
        )

        self.role_enum = role_enum
        self.model_id = ModelUtils.get_id()
        self.model = None
        self.deterministic = deterministic

    def set_model_path(self, model_path: str):
        self.model = ModelUtils.get_model(self.model_id, model_path)

    def get_speeds(
        self,
        environment,
        args: 'BehaviorArgs | None' = None
    ):
        if self.model is None:
            return 0, 0
        
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

    def reset(self):
        self.model = None