import numpy as np
from lib.domain.robot import Robot
from lib.domain.univector_field_navigation.obstacle import Obstacle
from lib.path_planning.univector_field_navigation import get_univector_field_point_theta
from lib.utils.geometry_utils import GeometryUtils
from configuration.configuration import Configuration
from lib.utils.robot_utils import RobotUtils

import math

KP = Configuration.motion_pid_constants_kp
KD = Configuration.motion_pid_constants_kd
K_TURNING = 0.443467
BASE_SPEED = Configuration.team_max_motor_speed

def wrap_to_pi(angle: float):
    pi = np.pi

    if angle > pi:
        return angle - 2 * pi
    if angle < -pi:
        return 2 * pi + angle
    else:
        return angle

def _is_close(robot: Robot, position: 'tuple[float, float]'):
    return GeometryUtils.is_close(
        robot.get_position_tuple(),
        position,
        .05)

class MotionUtils:
    @staticmethod
    def go_to_point(
        robot: Robot, 
        target_position: 'tuple[float, float]',
        last_error: float = 0,
        base_speed: float = BASE_SPEED
    ):
        if _is_close(robot, target_position):
            return 0, 0
    
        x, y = robot.get_position_tuple()
        robot_angle = robot.position.theta

        x_target, y_target = (target_position[0], target_position[1])

        angle_to_target = math.atan2(y_target - y, x_target - x)

        error = GeometryUtils.smallest_angle_difference(angle_to_target, robot_angle)

        if abs(error) > math.pi / 2.0 + math.pi / 20.0:
            reversed = True
            robot_angle = GeometryUtils.normalize_in_pi(robot_angle + math.pi)
            error = GeometryUtils.smallest_angle_difference(angle_to_target, robot_angle)
        else:
            reversed = False

        motorSpeed = (KP * error) + (KD * (error - last_error))

        motorSpeed = RobotUtils.truncate_motor_speed(motorSpeed, base_speed)

        leftMotorSpeed, rightMotorSpeed = MotionUtils._get_speeds(motorSpeed, base_speed, reversed)

        return leftMotorSpeed, rightMotorSpeed, error
    
    @staticmethod
    def go_to_point_2(
        position: 'tuple[float, float]',
        theta: 'float',
        target_position: 'tuple[float, float]',
        last_error: float = 0,
        base_speed: float = BASE_SPEED
    ):    
        x, y = position
        robot_angle = theta

        x_target, y_target = (target_position[0], target_position[1])

        angle_to_target = math.atan2(y_target - y, x_target - x)

        error = GeometryUtils.smallest_angle_difference(angle_to_target, robot_angle)

        if abs(error) > math.pi / 2.0 + math.pi / 20.0:
            reversed = True
            robot_angle = GeometryUtils.normalize_in_pi(robot_angle + math.pi)
            error = GeometryUtils.smallest_angle_difference(angle_to_target, robot_angle)
        else:
            reversed = False

        motorSpeed = (KP * error) + (KD * (error - last_error))

        motorSpeed = RobotUtils.truncate_motor_speed(motorSpeed, base_speed)

        leftMotorSpeed, rightMotorSpeed = MotionUtils._get_speeds(motorSpeed, base_speed, reversed)

        return leftMotorSpeed, rightMotorSpeed, error
    
    @staticmethod
    def go_to_point_by_theta(
        robot: Robot,
        theta: float,
        base_speed: float = BASE_SPEED
    ):
        vector = np.array([math.cos(theta), math.sin(theta)])

        speed = base_speed * np.linalg.norm(vector)
        angle_difference = wrap_to_pi(theta - robot.position.theta)
        
        motors_speeds = np.array([
            speed * math.cos(angle_difference),
            speed * math.cos(angle_difference)
        ])

        if angle_difference >= math.pi / 2 \
                or angle_difference <= -math.pi / 2:
            motors_speeds += np.array([
                speed * K_TURNING * math.sin(angle_difference),
                -speed * K_TURNING * math.sin(angle_difference)])
        else:
            motors_speeds += np.array([
                -speed * K_TURNING * math.sin(angle_difference),
                speed * K_TURNING * math.sin(angle_difference)])

        return motors_speeds
    
    @staticmethod
    def spin_to_theta(
        robot: Robot,
        theta_desired,
        base_speed: float = BASE_SPEED,
        tolerance=0.05
    ):
        theta_current = robot.position.theta
        theta_error = (theta_desired - theta_current + math.pi) % (2 * math.pi) - math.pi
        
        if abs(theta_error) < tolerance:
            return 0, 0

        if theta_error > 0:
            return MotionUtils.spin(False, base_speed * (theta_error / math.pi))
        else:
            return MotionUtils.spin(True, base_speed * (theta_error / math.pi))
    
    @staticmethod
    def go_to_point_univector(
        robot: Robot,
        target_position: 'tuple[float, float]',
        obstacles: 'tuple[Obstacle]',
        base_speed: float = BASE_SPEED,
        desired_theta: float = None
    ):
        if _is_close(robot, target_position):
            if desired_theta is None:
                return 0, 0
            else:
                return MotionUtils.spin_to_theta(robot, desired_theta, base_speed)

        theta = get_univector_field_point_theta(
            robot.get_position_tuple(),
            robot.get_velocity_tuple(),
            target_position,
            obstacles
        )

        return MotionUtils.go_to_point_by_theta(
            robot,
            theta,
            base_speed)

    @staticmethod
    def _get_speeds(
        motor_speed: float,
        base_speed: float,
        reversed: bool
    ):
        if reversed:
            if motor_speed > 0:
                left_motor_speed = -base_speed + motor_speed
                right_motor_speed = -base_speed
            else:
                left_motor_speed = -base_speed
                right_motor_speed = -base_speed - motor_speed
        else:
            if motor_speed > 0:
                left_motor_speed = base_speed
                right_motor_speed = base_speed - motor_speed
            else:
                left_motor_speed = base_speed + motor_speed
                right_motor_speed = base_speed

        return left_motor_speed, right_motor_speed
    
    @staticmethod
    def spin(clockwise: bool, spin_power: float):
        if clockwise:
            return spin_power, -spin_power
        
        return -spin_power, spin_power