import math
from lib.domain.robot import Robot
from lib.utils.geometry_utils import GeometryUtils
from lib.domain.ball import Ball

import numpy as np

class TrainingUtils():
    @staticmethod
    def r_speed(
        ball_past: Ball,
        ball_current: Ball,
        goal_position: 'tuple[float, float]'
    ):
        v = TrainingUtils.v(ball_past, ball_current, goal_position)
        return np.clip(v, -1, 1)
    
    @staticmethod
    def r_dist(
        robots: 'list[Robot]',
        ball: Ball
    ):
        min_distance = 0
        for robot in robots:
            distance = GeometryUtils.distance(
                robot.get_position_tuple(),
                ball.get_position_tuple())

            if min_distance == 0 or distance < min_distance:
                min_distance = distance

        return -1 if min_distance >= 1 else -min_distance

    @staticmethod
    def psi(
        a_position: 'tuple[float, float]',
        b_position: 'tuple[float, float]',
        c_position: 'tuple[float, float]'
    ):
        ba = np.array([
            b_position[0] - a_position[0],
            b_position[1] - a_position[1]
        ])
        bc = np.array([
            b_position[0] - c_position[0],
            b_position[1] - c_position[1]
        ])

        dot_product = np.dot(ba, bc)

        magnitude_ba = np.linalg.norm(ba)
        magnitude_bc = np.linalg.norm(bc)

        return np.arccos(dot_product / (magnitude_ba * magnitude_bc))

    @staticmethod
    def r_pos(
        a_position: 'tuple[float, float]',
        b_position: 'tuple[float, float]',
        c_position: 'tuple[float, float]'
    ):
        psi = TrainingUtils.psi(a_position, b_position, c_position)

        return psi / math.pi - 1.0

    @staticmethod
    def r_ofe(
        robot: Robot,
        ball: Ball,
        goal_opponent_position: 'tuple[float, float]'
    ):
        a_position = (robot.position.x, robot.position.y)
        b_position = (ball.position.x, ball.position.y)
        c_position = goal_opponent_position

        return 2 * (TrainingUtils.r_pos(a_position, b_position, c_position) + 1) - 1

    @staticmethod
    def r_def(
        robot: Robot,
        ball: Ball,
        own_goal_position: 'tuple[float, float]'
    ):
        a_position = (robot.position.x, robot.position.y)
        b_position = (ball.position.x, ball.position.y)
        c_position = own_goal_position

        return TrainingUtils.r_pos(a_position, b_position, c_position)

    # TODO: place constants in configuration.json
    @staticmethod
    def v(
        ball_past: Ball,
        ball_current: Ball,
        goal_position: 'tuple[float, float]'
    ):
        ball_past_position = ball_past.get_position_tuple()
        ball_current_position = ball_current.get_position_tuple()
        return (GeometryUtils.distance(ball_past_position, goal_position) - \
            GeometryUtils.distance(ball_current_position, goal_position) - 0.05) / 0.14

    @staticmethod
    def reward_attack(
        robotId: int,
        robots: 'list[Robot]',
        ball_past: Ball,
        ball_current: Ball,
        goal_position: 'tuple[float, float]'
    ):
        r_speed = TrainingUtils.r_speed(ball_past, ball_current, goal_position)
        r_dist = TrainingUtils.r_dist(robots, ball_current)
        rOfe = TrainingUtils.r_ofe(robots[robotId], ball_current, goal_position)

        return 0.7 * r_speed + 0.15 * r_dist + 0.15 * rOfe

    @staticmethod
    def reward_defense(
        robot_id: int,
        robots: 'list[Robot]',
        ball_past: Ball,
        ball_current: Ball,
        goal_position: 'tuple[float, float]',
        own_goal_position: 'tuple[float, float]'
    ):
        r_speed = TrainingUtils.r_speed(ball_past, ball_current, goal_position)
        r_dist = TrainingUtils.r_dist(robots, ball_current)
        r_def = TrainingUtils.r_def(robots[robot_id], ball_current, own_goal_position)

        return 0.7 * r_speed + 0.15 * r_dist + 0.15 * r_def

    @staticmethod
    def reward_goal(
        is_goal_made: bool,
        start_time: float,
        end_time: float
    ):
        return (10 if is_goal_made else -10) * (end_time - start_time) / end_time

    @staticmethod
    def reward_distance_robot_ball(
        robot: Robot,
        ball: Ball
    ):
        distance_robot_ball = GeometryUtils.distance(
            robot.get_position_tuple(),
            ball.get_position_tuple()
        )

        return -1 if distance_robot_ball >= 1 else 2 * (1 - distance_robot_ball) - 1

    @staticmethod
    def reward_angle_to_goal(
        robot: Robot,
        ball: Ball,
        opponent_goal_position: 'tuple[float, float]'
    ):
        robot_vector = GeometryUtils.get_vector_coordinates(
            robot.position.x,
            robot.position.y,
            robot.position.theta,
            1)

        vector1 = [robot_vector[0] - robot.position.x, robot_vector[1] - robot.position.y]
        vector2 = [opponent_goal_position[0] - ball.position.x, opponent_goal_position[1] - ball.position.y]

        return 2 * (1 - GeometryUtils.angle_between_vectors(vector1, vector2) / math.pi) - 1

    @staticmethod
    def reward_distance_ball_opponent_goal(
        ball: Ball,
        opponent_goal_position: 'tuple[float, float]'
    ):
        distance_ball_opponent_goal = GeometryUtils.distance(
            ball.get_position_tuple(),
            opponent_goal_position)

        if distance_ball_opponent_goal >= 1.5:
            return -1

        return 2 * (1.5 - distance_ball_opponent_goal) / 1.5 - 1
    