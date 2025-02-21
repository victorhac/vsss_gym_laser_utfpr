import random
import numpy as np

from rsoccer_gym.Entities import Frame, Robot, Ball
from rsoccer_gym.Utils import KDTree

from lib.behaviors.behavior_args import BehaviorArgs
from lib.domain.ball_curriculum_behavior import BallCurriculumBehavior
from lib.domain.curriculum_task import CurriculumTask
from lib.domain.enums.role_enum import RoleEnum
from lib.domain.robot_curriculum_behavior import RobotCurriculumBehavior
from lib.environment.base_environment import BaseEnvironment
from lib.position_setup.position_setup_args import PositionSetupArgs

from configuration.configuration import Configuration

TRAINING_EPISODE_DURATION = Configuration.rsoccer_training_episode_duration

NUMBER_ROBOTS_BLUE = Configuration.rsoccer_team_blue_number_robots
NUMBER_ROBOTS_YELLOW = Configuration.rsoccer_team_yellow_number_robots

V_WHEEL_DEADZONE = Configuration.rsoccer_robot_speed_dead_zone_meters_seconds

TIME_STEP = Configuration.rsoccer_training_time_step

# addapt this for your robot
MAX_MOTOR_SPEED = Configuration.firasim_robot_speed_max_radians_seconds

class BaseCurriculumEnvironment(BaseEnvironment):
    def __init__(
        self,
        task: CurriculumTask,
        render_mode="rgb_array",
        robot_id=0
    ):
        super().__init__(
            field_type=0,
            n_robots_blue=NUMBER_ROBOTS_BLUE,
            n_robots_yellow=NUMBER_ROBOTS_YELLOW,
            time_step=TIME_STEP,
            robot_id=robot_id,
            training_episode_duration=TRAINING_EPISODE_DURATION,
            render_mode=render_mode)

        self.max_motor_speed = MAX_MOTOR_SPEED
        self.v_wheel_deadzone = V_WHEEL_DEADZONE

        self.task = task

        self.previous_ball_potential = None
        self.last_game_score = None
        self.is_yellow_team = False
        self.is_left_team = True

    def reset(
        self,
        *,
        seed=None,
        options=None
    ):
        self.last_game_score = None
        return super().reset(seed=seed, options=options)
    
    def _create_robot_command_by_behavior(
        self,
        behavior: RobotCurriculumBehavior,
        role_enum: 'RoleEnum | None' = None
    ):
        args = BehaviorArgs(role_enum)
        left_speed, right_speed = behavior.behavior.get_speeds(self, args)

        return self._create_robot_command(
            behavior.robot_id,
            behavior.is_yellow,
            left_speed,
            right_speed)
    
    def _get_velocity_factor(self):
        rsoccer_max_motor_speed = self.max_v / self.field.rbt_wheel_radius
        return self.max_motor_speed / rsoccer_max_motor_speed

    def _actions_to_v_wheels(
        self,
        actions: np.ndarray
    ):
        left_wheel_speed = actions[0] * self.max_motor_speed
        right_wheel_speed = actions[1] * self.max_motor_speed

        if abs(left_wheel_speed * self.field.rbt_wheel_radius) < self.v_wheel_deadzone:
            left_wheel_speed = 0

        if abs(right_wheel_speed * self.field.rbt_wheel_radius) < self.v_wheel_deadzone:
            right_wheel_speed = 0

        return left_wheel_speed, right_wheel_speed
    
    def _get_commands(self, action):
        commands = []

        left_speed, right_speed = self._actions_to_v_wheels(action)

        robot = self._create_robot_command(
            self.robot_id,
            False,
            left_speed,
            right_speed)

        commands.append(robot)

        for i in range(self.n_robots_blue):
            if i == self.robot_id:
                continue

            behavior = self.task.get_blue_behaviors_by_robot_id(i)

            if behavior is None:
                commands.append(self._create_robot_command(i, False, 0, 0))
            else:
                commands.append(self._create_robot_command_by_behavior(behavior))

        for i in range(self.n_robots_yellow):
            behavior = self.task.get_yellow_behaviors_by_robot_id(i)

            if behavior is None:
                commands.append(self._create_robot_command(i, True, 0, 0))
            else:
                commands.append(self._create_robot_command_by_behavior(behavior))

        return commands

    def get_position_function_by_behavior(
        self,
        behavior: 'RobotCurriculumBehavior | BallCurriculumBehavior',
        relative_position: 'tuple[float, float] | None' = None
    ):
        args = PositionSetupArgs(behavior.distance, relative_position)
        return behavior.position_setup.get_position_function(args)

    def _get_initial_positions_frame(self):
        frame: Frame = Frame()
        places = KDTree()
        minimal_distance = 0.1

        def theta():
            return random.uniform(0, 360)

        def get_position(position_funcion):
            return BaseCurriculumEnvironment.get_position(
                places,
                minimal_distance,
                position_funcion)

        ball_position = self.get_position_function_by_behavior(self.task.ball_behavior)()

        places.insert(ball_position)

        frame.ball = Ball(x=ball_position[0], y=ball_position[1])

        for i in range(self.n_robots_blue):
            behavior = self.task.get_blue_behaviors_by_robot_id(i)

            if behavior is None:
                # this is a default position placed outside the field
                # in order for the robot to not interfere with the game
                # and do not appear in the render
                position = (10 + i, 10 + i)
            else:
                position_function = self.get_position_function_by_behavior(behavior, ball_position)
                position = get_position(position_function)

            frame.robots_blue[i] = Robot(
                x=position[0],
                y=position[1],
                theta=theta())

        for i in range(self.n_robots_yellow):
            behavior = self.task.get_yellow_behaviors_by_robot_id(i)

            if behavior is None:
                # this is a default position placed outside the field
                # in order for the robot to not interfere with the game
                # and do not appear in the render
                position = (20 + i, 20 + i)
            else:
                position_function = self.get_position_function_by_behavior(behavior, ball_position)
                position = get_position(position_function)

            frame.robots_yellow[i] = Robot(
                x=position[0],
                y=position[1],
                theta=theta())

        return frame

    def set_task(self, task: CurriculumTask):
        self.task = task
