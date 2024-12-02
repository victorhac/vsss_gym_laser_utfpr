from lib.domain.robot import Robot
from lib.utils.geometry_utils import GeometryUtils
from lib.utils.configuration_utils import ConfigurationUtils
from lib.utils.robot_utils import RobotUtils

import math

ROBOT_LENGTH = ConfigurationUtils.get_firasim_robot_length()
ROBOT_WIDTH = ConfigurationUtils.get_firasim_robot_width()

FIELD_WIDTH = ConfigurationUtils.get_field_width()
FIELD_LENGTH = ConfigurationUtils.get_field_length()

KP = ConfigurationUtils.get_motion_pid_constants_kp()
KD = ConfigurationUtils.get_motion_pid_constants_kd()

class MotionUtils:
    @staticmethod
    def go_to_point(
        robot: Robot, 
        target_position: 'tuple[float, float]',
        last_error: float = 0,
        base_speed: float = 30
    ):
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

        motorSpeed = RobotUtils.truncateMotorSpeed(motorSpeed, base_speed)

        leftMotorSpeed, rightMotorSpeed = MotionUtils._get_speeds(motorSpeed, base_speed, reversed)

        return leftMotorSpeed, rightMotorSpeed, error

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