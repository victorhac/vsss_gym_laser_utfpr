from lib.behaviors.behavior import Behavior
from lib.behaviors.behavior_args import BehaviorArgs

class FromModelBehavior(Behavior):
    def __init__(
        self,
        robot_id: int,
        is_yellow: bool
    ):
        super().__init__(
            robot_id,
            is_yellow
        )

    def get_speeds(
        self,
        environment,
        args: 'BehaviorArgs | None' = None
    ):
        return 0, 0