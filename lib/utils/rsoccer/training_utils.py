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

def _r_ofe(
    robot: Robot,
    ball: Ball,
    goal_opponent_position: 'tuple[float, float]'
):
    a_position = robot.x, robot.y
    b_position = ball.x, ball.y
    c_position = goal_opponent_position

    return _r_pos(a_position, b_position, c_position)

def _r_speed(
    ball: Ball,
    ball_past: Ball,
    goal_position: 'tuple[float, float]'
):
    return np.clip(
        v(ball, ball_past, goal_position),
        -1,
        1
    )

def _r_dist(
    robots: 'list[Robot]',
    ball: Ball
):
    min_distance = 0
    for robot in robots:
        distance = GeometryUtils.distance(
            (robot.x, robot.y),
            (ball.x, ball.y))

        if min_distance == 0 or distance < min_distance:
            min_distance = distance

    return -1 if min_distance >= 1 else -min_distance

def v(
    ball: Ball,
    past_ball: Ball,
    goal_position: 'tuple[float, float]'
):
    past_ball_position = past_ball.x, past_ball.y
    ball_position = ball.x, ball.y
    return (GeometryUtils.distance(past_ball_position, goal_position) - \
        GeometryUtils.distance(ball_position, goal_position) - 0.05) / 0.14

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
    def get_offensive_positioning_reward(
        robot: Robot,
        ball: Ball,
        goal_opponent_position: 'tuple[float, float]'
    ):
        return _r_ofe(
            robot,
            ball,
            goal_opponent_position
        )
    
    @staticmethod
    def get_speed_reward(
        ball: Ball,
        ball_past: Ball,
        goal_position: 'tuple[float, float]'
    ):
        return _r_speed(
            ball,
            ball_past,
            goal_position
        )
    
    @staticmethod
    def get_distance_reward(
        robots: 'list[Robot]',
        ball: Ball
    ):
        return _r_dist(
            robots,
            ball
        )
    
    @staticmethod
    def get_team_reward(
        robots: 'list[Robot]',
        ball: Ball,
        ball_past: Ball,
        own_goal_position: 'tuple[float, float]',
        opponent_goal_position: 'tuple[float, float]'
    ):
        max_r_def = None
        max_r_ofe = None
    
        for i in robots:
            r_def = _r_def(
                i,
                ball,
                own_goal_position
            )
            r_ofe = _r_ofe(
                i,
                ball,
                opponent_goal_position
            )
    
            if max_r_def is None or r_def > max_r_def:
                max_r_def = r_def
    
            if max_r_ofe is None or r_ofe > max_r_ofe:
                max_r_ofe = r_ofe
        
        return max_r_ofe + \
            max_r_def + \
            _r_speed(
                ball,
                ball_past,
                own_goal_position
            ) + _r_dist(
                robots,
                ball
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