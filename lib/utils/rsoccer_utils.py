from .configuration_utils import ConfigurationUtils
from ..domain.field_data import FieldData
from ..domain.robot import Robot
from ..domain.ball import Ball
from ..geometry.geometry_utils import GeometryUtils

from rsoccer_gym.Entities import Robot as RSoccerRobot, Ball as RSoccerBall
from rsoccer_gym.Entities.Frame import Frame

import numpy as np

class RSoccerUtils:
    GOAL_DEPTH = ConfigurationUtils.get_field_goal_depth()
    FIELD_WIDTH = ConfigurationUtils.get_field_width()
    FIELD_LENGTH = ConfigurationUtils.get_field_length()

    ROBOT_WHEEL_RADIUS = ConfigurationUtils.get_rsoccer_robot_wheel_radius()
    ROBOT_MAX_RPM = ConfigurationUtils.get_rsoccer_robot_motor_max_rpm()
    V_WHEEL_DEADZONE = ConfigurationUtils.get_rsoccer_robot_speed_dead_zone_meters_seconds()
    MAX_V = (ROBOT_MAX_RPM / 60) * 2 * np.pi * ROBOT_WHEEL_RADIUS

    @staticmethod
    def get_corrected_angle(angle: float):
        angleRadians = np.deg2rad(angle)
        return GeometryUtils.normalize_in_pi(angleRadians)

    @staticmethod
    def to_robot(rSoccerRobot: RSoccerRobot):
        robot = Robot()

        robot.position.x = rSoccerRobot.x
        robot.position.y = rSoccerRobot.y
        robot.position.theta = RSoccerUtils.get_corrected_angle(rSoccerRobot.theta)

        robot.velocity.x = rSoccerRobot.v_x
        robot.velocity.y = rSoccerRobot.v_y
        robot.velocity.theta = RSoccerUtils.get_corrected_angle(rSoccerRobot.v_theta)
        
        return robot
    
    @staticmethod
    def to_ball(rSoccerBall: RSoccerBall):
        ball = Ball()

        ball.position.x = rSoccerBall.x
        ball.position.y = rSoccerBall.y
        ball.velocity.x = rSoccerBall.v_x
        ball.velocity.y = rSoccerBall.v_y

        return ball
    
    @staticmethod
    def get_rsoccer_robot_action(
        id: int,
        isYellowTeam: bool,
        leftMotorSpeed: float,
        rightMotorSpeed: float
    ):
        return RSoccerRobot(
            yellow=isYellowTeam,
            id=id,
            v_wheel0=leftMotorSpeed,
            v_wheel1=rightMotorSpeed
        )
    
    @staticmethod
    def get_field_datas(next_state, isYellowTeam: bool):
        fieldData = FieldData()
        opponentFieldData = FieldData()

        ball = RSoccerUtils.to_ball(next_state[0])

        blueTeam = []
        yellowTeam = []

        for i in range(1, len(next_state)):
            robot = next_state[i]
            if robot.yellow is not None:
                if robot.yellow:
                    yellowTeam.append(RSoccerUtils.to_robot(robot))
                else:
                    blueTeam.append(RSoccerUtils.to_robot(robot))

        fieldData.ball = ball
        opponentFieldData.ball = ball

        if isYellowTeam:
            fieldData.robots = yellowTeam
            fieldData.foes = blueTeam

            opponentFieldData.robots = blueTeam
            opponentFieldData.foes = yellowTeam
        else:
            fieldData.robots = blueTeam
            fieldData.foes = yellowTeam

            opponentFieldData.robots = yellowTeam
            opponentFieldData.foes = blueTeam

        return fieldData, opponentFieldData
    
    @staticmethod
    def get_field_data(frame: Frame, is_yellow_team: bool):
        field_data = FieldData()

        ball = RSoccerUtils.to_ball(frame.ball)

        blue_team = [RSoccerUtils.to_robot(frame.robots_blue[i]) for i in frame.robots_blue]
        yellow_team = [RSoccerUtils.to_robot(frame.robots_yellow[i]) for i in frame.robots_yellow]

        field_data.ball = ball

        if is_yellow_team:
            field_data.robots = yellow_team
            field_data.foes = blue_team
        else:
            field_data.robots = blue_team
            field_data.foes = yellow_team

        return field_data

    def norm_v(v):
        return np.clip(v * 1.25 / RSoccerUtils.MAX_V, -1, 1)
    
    def norm_x(x):
        return np.clip(x / RSoccerUtils.get_max_x(), -1, 1)
    
    def norm_y(y):
        return np.clip(y / RSoccerUtils.get_max_y(), -1, 1)
    
    def get_max_x():
        return RSoccerUtils.FIELD_LENGTH / 2 + RSoccerUtils.GOAL_DEPTH
    
    def get_max_y():
        return RSoccerUtils.FIELD_WIDTH / 2
    
    @staticmethod
    def get_attacker_observation(
        field_data: FieldData,
        is_left_team: bool,
        robot_id: int
    ):
        return RSoccerUtils.get_default_observation(field_data, is_left_team, robot_id)
    
    @staticmethod
    def get_defensor_observation(
        field_data: FieldData,
        is_left_team: bool,
        robot_id: int
    ):
        return RSoccerUtils.get_default_observation(field_data, is_left_team, robot_id)

    @staticmethod
    def get_robot_observation(
        is_left_team: bool,
        robot: Robot
    ):
        def norm_x(x): return RSoccerUtils.norm_x(x)
        def norm_y(y): return RSoccerUtils.norm_y(y)
        def norm_v(v): return RSoccerUtils.norm_v(v)

        position = robot.position
        velocity = robot.velocity
        theta = position.theta

        return [
            norm_x(position.x),
            norm_y(position.y),
            theta / np.pi,
            norm_v(velocity.x),
            norm_v(velocity.y)
        ]
    
    @staticmethod
    def get_ball_observation(
        field_data: FieldData,
        is_left_team: bool
    ):
        ball = field_data.ball

        def norm_x(x): return RSoccerUtils.norm_x(x)
        def norm_y(y): return RSoccerUtils.norm_y(y)
        def norm_v(v): return RSoccerUtils.norm_v(v)

        position = ball.position
        velocity = ball.velocity

        return [
            norm_x(position.x),
            norm_y(position.y),
            norm_v(velocity.x),
            norm_v(velocity.y)
        ]
    
    @staticmethod
    def get_default_observation(
        field_data: FieldData,
        is_left_team: bool,
        robot_id: int
    ):
        observation = []

        observation.extend(RSoccerUtils.get_ball_observation(field_data, is_left_team))

        robot = field_data.robots[robot_id]
        observation.extend(RSoccerUtils.get_robot_observation(is_left_team, robot))

        robot = field_data.foes[0]
        observation.extend(RSoccerUtils.get_robot_observation(is_left_team, robot))

        return np.array(observation, dtype=np.float32)
    
    @staticmethod
    def actions_to_v_wheels(
        actions: np.ndarray,
        is_own_team: bool
    ):
        max_v = RSoccerUtils.MAX_V
        rbt_wheel_radius = RSoccerUtils.ROBOT_WHEEL_RADIUS

        # the actions were switched because rsoccer uses a different convention
        left_wheel_speed = actions[1] * max_v
        right_wheel_speed = actions[0] * max_v

        left_wheel_speed, right_wheel_speed = np.clip(
            (left_wheel_speed, right_wheel_speed),
            -max_v,
            max_v)
        
        if is_own_team:
            factor = 30 / (max_v / rbt_wheel_radius)
        else:
            factor = 1

        left_wheel_speed *= factor
        right_wheel_speed *= factor

        v_wheel_deadzone = RSoccerUtils.V_WHEEL_DEADZONE

        if abs(left_wheel_speed) < v_wheel_deadzone:
            left_wheel_speed = 0

        if abs(right_wheel_speed) < v_wheel_deadzone:
            right_wheel_speed = 0

        left_wheel_speed /= rbt_wheel_radius
        right_wheel_speed /= rbt_wheel_radius

        return left_wheel_speed, right_wheel_speed