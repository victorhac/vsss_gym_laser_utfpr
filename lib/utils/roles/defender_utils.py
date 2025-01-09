from rsoccer_gym.Entities import Robot as RSoccerRobot
from lib.domain.field import Field
from lib.domain.field import Robot
from lib.environment.base_environment import BaseEnvironment
from lib.utils.rsoccer_utils import RSoccerUtils
from stable_baselines3 import PPO
import numpy as np

class DefenderUtils:
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
            return RSoccerUtils.get_x_and_y(x, y, is_left_team)
        
        def get_norm_theta(robot: RSoccerRobot):
            return RSoccerUtils.get_norm_theta_by_rsoccer_robot(robot, is_left_team)

        def extend_observation_by_ball():
            x, y = get_x_and_y(ball.x, ball.y)
            v_x, v_y = get_x_and_y(ball.v_x, ball.v_y)

            observation.extend([
                base_environment.norm_x(x),
                base_environment.norm_y(y),
                base_environment.norm_v(v_x),
                base_environment.norm_v(v_y)
            ])

        def extend_observation_by_robot(robot: RSoccerRobot):
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

        team, foe_team = RSoccerUtils.get_team_and_foe_team(base_environment, is_yellow)

        extend_observation_by_robot(team[robot_id])

        for i in range(3):
            if i == robot_id:
                continue

            extend_observation_by_robot(team[i])

        for i in range(3):
            extend_observation_by_robot(foe_team[i])

        return np.array(observation, dtype=np.float32)
    
    @staticmethod
    def get_observation_by_field(
        field: Field,
        robot_id: int,
        is_left_team: bool
    ):
        observation = []

        ball = field.ball
        
        def get_norm_theta(robot: Robot):
            return RSoccerUtils.get_norm_theta_by_robot(robot, is_left_team)
        
        def get_x_and_y(x: float, y: float):
            return RSoccerUtils.get_x_and_y(x, y, is_left_team)
        
        def norm_v(v: float):
            return RSoccerUtils.norm_v(v)
        
        def norm_x(x: float):
            return RSoccerUtils.norm_x(x)
        
        def norm_y(y: float):
            return RSoccerUtils.norm_y(y)
        
        def is_inside_field(x: float, y: float):
            return RSoccerUtils.is_inside_field(x, y)

        def extend_observation_by_ball():
            x, y = get_x_and_y(ball.position.x, ball.position.y)
            v_x, v_y = get_x_and_y(ball.velocity.x, ball.velocity.y)

            observation.extend([
                norm_x(x),
                norm_y(y),
                norm_v(v_x),
                norm_v(v_y)
            ])

        def extend_observation_by_robot(robot: Robot):
            x, y = get_x_and_y(robot.position.x, robot.position.y)
            v_x, v_y = get_x_and_y(robot.velocity.x, robot.velocity.y)

            if is_inside_field((x, y)): 
                observation.extend([
                    norm_x(x),
                    norm_y(y),
                    get_norm_theta(robot),
                    norm_v(v_x),
                    norm_v(v_y)
                ])
            else:
                observation.extend([0, 0, 0, 0, 0])

        extend_observation_by_ball()

        extend_observation_by_robot(field.robots[robot_id])

        for i in range(3):
            if i == robot_id:
                continue

            extend_observation_by_robot(field.robots[i])

        for i in range(3):
            extend_observation_by_robot(field.foes[i])

        return np.array(observation, dtype=np.float32)

    @staticmethod
    def get_speeds_by_field(
        field: Field,
        robot_id: int,
        is_left_team: bool,
        model: PPO
    ):
        observation = DefenderUtils.get_observation_by_field(
            field,
            robot_id,
            is_left_team
        )

        action, _ = model.predict(observation)

        return RSoccerUtils.actions_to_v_wheels(action)
