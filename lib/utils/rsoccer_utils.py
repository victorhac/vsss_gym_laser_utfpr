from configuration.configuration import Configuration
from lib.domain.field import Field
from lib.domain.robot import Robot
from lib.domain.ball import Ball
from lib.utils.domain_utils import DomainUtils
from lib.utils.field_utils import FieldUtils
from lib.utils.geometry_utils import GeometryUtils

from rsoccer_gym.Entities import Robot as RSoccerRobot, Ball as RSoccerBall
from rsoccer_gym.Entities.Frame import Frame

import numpy as np

class RSoccerUtils:
    @staticmethod
    def get_corrected_angle(angle: float):
        angleRadians = np.deg2rad(angle)
        return GeometryUtils.normalize_in_pi(angleRadians)

    @staticmethod
    def to_robot(rsoccer_robot: RSoccerRobot):
        robot = Robot()

        robot.position.x = rsoccer_robot.x
        robot.position.y = rsoccer_robot.y
        robot.position.theta = RSoccerUtils.get_corrected_angle(rsoccer_robot.theta)

        robot.velocity.x = rsoccer_robot.v_x
        robot.velocity.y = rsoccer_robot.v_y
        robot.velocity.theta = RSoccerUtils.get_corrected_angle(rsoccer_robot.v_theta)

        return robot

    @staticmethod
    def to_ball(rsoccer_ball: RSoccerBall):
        ball = Ball()

        ball.position.x = rsoccer_ball.x
        ball.position.y = rsoccer_ball.y
        ball.velocity.x = rsoccer_ball.v_x
        ball.velocity.y = rsoccer_ball.v_y

        return ball

    @staticmethod
    def get_field_by_frame(frame: Frame, is_yellow_team: bool):
        field_data = Field()

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
    
    @staticmethod
    def _get_rendering_frame_by_frame(frame: Frame):
        rendering_frame = Frame()

        def get_robot(source_robot):
            return RSoccerUtils._get_robot_inverted_y_axis(source_robot)
        
        def get_ball():
            return RSoccerUtils._get_ball_inverted_y_axis(frame)

        for item in frame.robots_blue:
            rendering_frame.robots_blue[item] = get_robot(
                frame.robots_blue[item]
            )

        for item in frame.robots_yellow:
            rendering_frame.robots_yellow[item] = get_robot(
                frame.robots_yellow[item]
            )

        rendering_frame.ball = get_ball()

        return rendering_frame
    
    @staticmethod
    def _get_frame_by_rendering_frame(rendering_frame: Frame):
        frame = Frame()

        def get_robot(source_robot):
            return RSoccerUtils._get_robot_inverted_y_axis(source_robot)
        
        def get_ball():
            return RSoccerUtils._get_ball_inverted_y_axis(rendering_frame)

        for item in rendering_frame.robots_blue:
            frame.robots_blue[item] = get_robot(
                rendering_frame.robots_blue[item]
            )

        for item in rendering_frame.robots_yellow:
            frame.robots_yellow[item] = get_robot(
                rendering_frame.robots_yellow[item]
            )

        frame.ball = get_ball()

        return frame
    
    @staticmethod
    def _get_robot_inverted_y_axis(source_robot: RSoccerRobot):
        robot = RSoccerRobot()
        DomainUtils.copy(source_robot, robot)
        robot.y = -robot.y
        robot.v_y = -robot.v_y
        robot.theta = RSoccerUtils.get_angle_inverted_y_axis(robot.theta)
        return robot

    @staticmethod 
    def _get_ball_inverted_y_axis(frame: Frame):
        source_ball = frame.ball
        ball = RSoccerBall()
        DomainUtils.copy(source_ball, ball)
        ball.y = -ball.y
        return ball
    
    @staticmethod
    def get_angle_inverted_y_axis(theta: float):
        theta = theta % 360
        theta = (360 - theta) % 360
        if theta < 0:
            theta += 360
        return theta

    @staticmethod
    def get_x_and_y(
        x: float,
        y: float,
        is_left_team: bool
    ):
        if is_left_team:
            return x, y
        return -x, -y
    
    @staticmethod
    def get_norm_theta_by_rsoccer_robot(robot: RSoccerRobot, is_left_team: bool):
        if is_left_team:
            return RSoccerUtils.get_corrected_angle(robot.theta) / np.pi
        
        theta = RSoccerUtils.get_corrected_angle(robot.theta)

        if theta < 0:
            theta += np.pi
        elif theta > 0:
            theta -= np.pi

        return theta / np.pi
    
    @staticmethod
    def get_team_and_foe_team(
        environment,
        is_yellow: bool
    ):
        frame = environment.frame

        team = frame.robots_yellow if is_yellow else frame.robots_blue
        foe_team = frame.robots_blue if is_yellow else frame.robots_yellow

        return team, foe_team

    @staticmethod
    def get_normalized_distance(distance: float):
        return np.clip(distance / Configuration.rsoccer_training_max_distance, -1, 1)
    
    @staticmethod
    def norm_v(v: float):
        return np.clip(v / Configuration.rsoccer_training_max_v, -1, 1)
    
    @staticmethod
    def norm_x(x: float):
        return np.clip(x / Configuration.rsoccer_training_max_x, -1, 1)
    
    @staticmethod
    def norm_y(y: float):
        return np.clip(y / Configuration.rsoccer_training_max_y, -1, 1)
    
    @staticmethod
    def is_inside_field(x: float, y: float):
        return FieldUtils.is_inside_field(
            x,
            y,
            Configuration.field_length,
            Configuration.field_width,
            Configuration.field_goal_width,
            Configuration.field_goal_depth)
    
    @staticmethod
    def get_velocity_factor():
        max_v = Configuration.rsoccer_training_max_v
        rbt_wheel_radius = Configuration.rsoccer_robot_wheel_radius
        max_motor_speed = Configuration.firasim_robot_speed_max_radians_seconds

        rsoccer_max_motor_speed = max_v / rbt_wheel_radius

        return max_motor_speed / rsoccer_max_motor_speed

    @staticmethod
    def actions_to_v_wheels(actions: np.ndarray):
        max_v = Configuration.rsoccer_training_max_v
        v_wheel_deadzone = Configuration.rsoccer_robot_speed_dead_zone_meters_seconds

        left_wheel_speed = actions[0] * max_v
        right_wheel_speed = actions[1] * max_v

        left_wheel_speed, right_wheel_speed = np.clip(
            (left_wheel_speed, right_wheel_speed),
            -max_v,
            max_v)

        factor = RSoccerUtils.get_velocity_factor()

        left_wheel_speed *= factor
        right_wheel_speed *= factor

        if abs(left_wheel_speed) < v_wheel_deadzone:
            left_wheel_speed = 0

        if abs(right_wheel_speed) < v_wheel_deadzone:
            right_wheel_speed = 0

        rbt_wheel_radius = Configuration.rsoccer_robot_wheel_radius

        left_wheel_speed /= rbt_wheel_radius
        right_wheel_speed /= rbt_wheel_radius

        return right_wheel_speed, left_wheel_speed
