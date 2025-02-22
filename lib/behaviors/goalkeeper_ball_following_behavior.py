import numpy as np
from lib.behaviors.behavior import Behavior
from lib.behaviors.behavior_args import BehaviorArgs
from lib.utils.motion_utils import MotionUtils
from lib.utils.rsoccer.rsoccer_utils import RSoccerUtils

class GoalkeeperBallFollowingBehavior(Behavior):
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

        if environment._is_inside_own_goal_area((ball.x, ball.y), self.is_yellow):
            left_speed, right_speed, self.error = MotionUtils.go_to_point_2(
                (robot.x, robot.y),
                theta,
                (ball.x, ball.y),
                self.error,
                environment.max_motor_speed)
        else:
            max_y = environment.get_goal_area_width() / 2
            x = environment.get_field_length() / 2 - environment.get_goal_area_length() / 2

            x = x if self.is_yellow else -x
            y = np.clip(ball.y, -max_y, max_y)

            position = x, y

            if environment._is_close_to_position(robot, position):
                left_speed, right_speed = 0, 0
            else:
                left_speed, right_speed, self.error = MotionUtils.go_to_point_2(
                    (robot.x, robot.y),
                    theta,
                    position,
                    self.error,
                    environment.max_motor_speed)

        return self._get_final_speeds(left_speed, right_speed)
