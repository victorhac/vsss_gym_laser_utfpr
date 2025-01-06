from rsoccer_gym.Entities import Robot

from lib.environment.base_environment import BaseEnvironment
from lib.utils.environment.environment_utils import EnvironmentUtils

import numpy as np

class DefenderEnvironmentUtils:
    @staticmethod
    def get_observation(
        base_environment: BaseEnvironment,
        robot_id: int,
        is_yellow: bool,
        is_left_team: bool
    ):
        observation = []

        ball = base_environment._get_ball()

        def get_x_and_y(x: float, y: float):
            return EnvironmentUtils.get_x_and_y(x, y, is_left_team)
        
        def get_norm_theta(robot: Robot):
            return EnvironmentUtils.get_norm_theta(robot, is_left_team)

        def extend_observation_by_ball():
            x, y = get_x_and_y(ball.x, ball.y)
            v_x, v_y = get_x_and_y(ball.v_x, ball.v_y)

            observation.extend([
                base_environment.norm_x(x),
                base_environment.norm_y(y),
                base_environment.norm_v(v_x),
                base_environment.norm_v(v_y)
            ])

        def extend_observation_by_robot(robot: Robot):
            theta = get_norm_theta(robot)
            x, y = get_x_and_y(robot.x, robot.y)
            v_x, v_y = get_x_and_y(robot.v_x, robot.v_y)

            if base_environment._is_inside_field((x, y)): 
                observation.extend([
                    base_environment.norm_x(x),
                    base_environment.norm_y(y),
                    theta,
                    base_environment.norm_v(v_x),
                    base_environment.norm_v(v_y)
                ])
            else:
                observation.extend([0, 0, 0, 0, 0])

        extend_observation_by_ball()

        team, foe_team = EnvironmentUtils.get_team_and_foe_team(base_environment, is_yellow)

        extend_observation_by_robot(team[robot_id])

        for i in range(3):
            if i == robot_id:
                continue

            extend_observation_by_robot(team[i])

        for i in range(3):
            extend_observation_by_robot(foe_team[i])

        return np.array(observation, dtype=np.float32)
