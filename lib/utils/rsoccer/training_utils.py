import math
from configuration.configuration import Configuration
from lib.utils.geometry_utils import GeometryUtils
from rsoccer_gym.Entities import Robot, Ball

import numpy as np

def _psi(
    position_a: 'tuple[float, float]',
    position_b: 'tuple[float, float]',
    position_c: 'tuple[float, float]'
):
    ba = np.array([
        position_b[0] - position_a[0],
        position_b[1] - position_a[1]
    ])
    bc = np.array([
        position_b[0] - position_c[0],
        position_b[1] - position_c[1]
    ])

    dot_product = np.dot(ba, bc)

    magnitude_ba = np.linalg.norm(ba)
    magnitude_bc = np.linalg.norm(bc)

    return np.arccos(dot_product / (magnitude_ba * magnitude_bc))

def _r_pos(
    position_a: 'tuple[float, float]',
    position_b: 'tuple[float, float]',
    position_c: 'tuple[float, float]'
):
    psi_value = _psi(position_a, position_b, position_c)

    return psi_value / math.pi - 1.0

def _r_def(
    robot: Robot,
    ball: Ball,
    own_goal_position: 'tuple[float, float]'
):
    a_position = own_goal_position
    b_position = robot.x, robot.y
    c_position = ball.x, ball.y

    return _r_pos(a_position, b_position, c_position)

class TrainingUtils:
    @staticmethod
    def get_defensive_positioning_reward(
        robot: Robot,
        ball: Ball,
        own_goal_position: 'tuple[float, float]'
    ):
        return _r_def(
            robot,
            ball,
            own_goal_position
        )

    @staticmethod
    def get_gradient_reward(
        ball: Ball,
        desired_position: float,
        undesired_position: float,
        previous_ball_potential: 'float | None',
        max_distance: float = Configuration.field_length,
        range: 'tuple[float, float]' = (-5.0, 5.0)
    ):
        time_step = Configuration.rsoccer_training_time_step

        distance_to_desired = GeometryUtils.distance(
            (ball.x, ball.y),
            desired_position)
            
        distance_to_undesired = GeometryUtils.distance(
            (ball.x, ball.y),
            undesired_position)

        ball_potential = ((distance_to_undesired - distance_to_desired) / max_distance - 1) / 2

        if previous_ball_potential is not None:
            ball_potential_difference = ball_potential - previous_ball_potential
            reward = np.clip(
                ball_potential_difference * 3 / time_step,
                range[0],
                range[1])
        else:
            reward = 0

        return reward, ball_potential
    
    def get_move_reward(
        robot: Robot,
        position: 'tuple[float, float]',
        range: 'tuple[float, float]' = (-5.0, 5.0)
    ):
        robot_position = np.array([robot.x, robot.y])
        robot_velocities = np.array([robot.v_x, robot.v_y])

        robot_target_vector = np.array(position) - robot_position
        robot_target_vector = robot_target_vector / np.linalg.norm(robot_target_vector)

        move_reward = np.dot(robot_target_vector, robot_velocities)

        return np.clip(move_reward / 0.4, range[0], range[1])