from lib.curriculum.behaviors.behavior import Behavior
from lib.domain.behavior_args import BehaviorArgs
from lib.utils.motion_utils import MotionUtils
from lib.utils.rsoccer.rsoccer_utils import RSoccerUtils

class BallFollowingBehavior(Behavior):
    def __init__(
        self,
        robot_id: int,
        is_yellow: bool
    ):
        super().__init__(
            robot_id,
            is_yellow
        )

        self.error = 0

    def get_speeds(
        self,
        environment,
        args: 'BehaviorArgs | None' = None
    ):
        robot = self._get_robot(environment)
        ball = environment._get_ball()
        
        theta = RSoccerUtils.get_corrected_angle(robot.theta)

        left_speed, right_speed, self.error = MotionUtils.go_to_point_2(
            (robot.x, robot.y),
            theta,
            (ball.x, ball.y),
            self.error,
            environment.max_motor_speed)

        return self._get_final_speeds(left_speed, right_speed)
