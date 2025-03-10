from rsoccer_gym.Entities import Robot as RSoccerRobot
from lib.domain.field import Field
from lib.domain.robot import Robot
from lib.environment.base_environment import BaseEnvironment
from lib.utils.rsoccer.rsoccer_utils import RSoccerUtils
import numpy as np
from stable_baselines3 import PPO

class GoalkeeperUtils:
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
            x, y = get_x_and_y(robot.x, robot.y)
            v_x, v_y = get_x_and_y(robot.v_x, robot.v_y)

            if base_environment._is_inside_field((x, y)): 
                observation.extend([
                    base_environment.norm_x(x),
                    base_environment.norm_y(y),
                    get_norm_theta(robot),
                    base_environment.norm_v(v_x),
                    base_environment.norm_v(v_y)
                ])
            else:
                observation.extend([0, 0, 0, 0, 0])

        extend_observation_by_ball()

        team, _ = RSoccerUtils.get_team_and_foe_team(base_environment, is_yellow)

        extend_observation_by_robot(team[robot_id])

        return np.array(observation, dtype=np.float32)
    
    @staticmethod
    def get_observation_by_field(
        field: Field,
        robot_id: int
    ):
        observation = []
        ball = field.ball
        
        def get_norm_theta(robot: Robot):
            return robot.position.theta / np.pi
        
        def norm_v(v: float):
            return RSoccerUtils.norm_v(v)
        
        def norm_x(x: float):
            return RSoccerUtils.norm_x(x)
        
        def norm_y(y: float):
            return RSoccerUtils.norm_y(y)
        
        def is_inside_field(robot: Robot):
            return RSoccerUtils.is_inside_field(robot.position.x, robot.position.y)

        def extend_observation_by_ball():
            observation.extend([
                norm_x(ball.position.x),
                norm_y(ball.position.y),
                norm_v(ball.velocity.x),
                norm_v(ball.velocity.y)
            ])

        def extend_observation_by_robot(robot: Robot):
            if is_inside_field(robot): 
                observation.extend([
                    norm_x(robot.position.x),
                    norm_y(robot.position.y),
                    get_norm_theta(robot),
                    norm_v(robot.velocity.x),
                    norm_v(robot.velocity.y)
                ])
            else:
                observation.extend([0, 0, 0, 0, 0])

        extend_observation_by_ball()

        extend_observation_by_robot(field.get_robot_by_id(robot_id))

        return np.array(observation, dtype=np.float32)

    @staticmethod
    def get_speeds_by_field(
        field: Field,
        robot_id: int,
        model: PPO,
        deterministic: bool = True
    ):
        observation = GoalkeeperUtils.get_observation_by_field(
            field,
            robot_id
        )

        action, _ = model.predict(observation, deterministic=deterministic)

        return RSoccerUtils.actions_to_v_wheels(action)
    
    @staticmethod
    def get_speeds(
        base_environment: BaseEnvironment,
        robot_id: int,
        is_yellow: bool,
        is_left_team: bool,
        model: PPO,
        deterministic: bool = True
    ):
        observation = GoalkeeperUtils.get_observation(
            base_environment,
            robot_id,
            is_yellow,
            is_left_team
        )

        action = model.predict(observation, deterministic=deterministic)[0]

        return RSoccerUtils.actions_to_v_wheels(action)
