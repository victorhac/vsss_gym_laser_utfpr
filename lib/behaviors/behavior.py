from lib.behaviors.behavior_args import BehaviorArgs

class Behavior:
    def __init__(
        self,
        robot_id: int,
        is_yellow: bool,
    ):
        self.robot_id = robot_id
        self.is_yellow = is_yellow
        self.velocity_alpha = 1

    def get_speeds(
        self,
        environment,
        args: 'BehaviorArgs | None' = None
    ):
        raise NotImplementedError()
    
    def _get_robot(
        self,
        environment
    ):
        return environment._get_robot_by_id(
            self.robot_id,
            self.is_yellow
        )
    
    def reset(self):
        pass

    def _get_final_speeds(
        self,
        left_speed: float,
        right_speed: float
    ):
        return left_speed * self.velocity_alpha, right_speed * self.velocity_alpha