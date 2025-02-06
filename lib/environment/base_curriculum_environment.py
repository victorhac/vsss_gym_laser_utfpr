import random
import numpy as np

from rsoccer_gym.Entities import Frame, Robot, Ball
from rsoccer_gym.Utils import KDTree
from stable_baselines3 import PPO

from lib.domain.ball_curriculum_behavior import BallCurriculumBehavior
from lib.domain.curriculum_task import CurriculumTask
from lib.domain.enums.robot_curriculum_behavior_enum import RobotCurriculumBehaviorEnum
from lib.domain.enums.role_enum import RoleEnum
from lib.domain.robot_curriculum_behavior import RobotCurriculumBehavior
from lib.environment.base_environment import BaseEnvironment
from lib.position_setup.position_setup_args import PositionSetupArgs
from lib.positioning.default_supporter_positioning import get_supporter_position
from lib.utils.field_utils import FieldUtils
from lib.utils.model_utils import ModelUtils
from lib.utils.motion_utils import MotionUtils

from configuration.configuration import Configuration
from lib.utils.roles.attacker.attacker_v2_utils import AttackerV2Utils
from lib.utils.roles.attacker_utils import AttackerUtils
from lib.utils.roles.defender_utils import DefenderUtils
from lib.utils.roles.goalkeeper_utils import GoalkeeperUtils
from lib.utils.rsoccer.rsoccer_utils import RSoccerUtils

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

        self._set_error_dictionaries()
        self._set_model_id_dictionaries()

    def _set_error_dictionaries(self):
        self.own_team_error_dictionary = {
            0: .0,
            1: .0,
            2: .0,
        }

        self.opponent_error_dictionary = {
            0: .0,
            1: .0,
            2: .0
        }

    def _set_model_id_dictionaries(self):
        self.own_team_model_id_dictionary = {
            0: ModelUtils.get_id(),
            1: ModelUtils.get_id(),
            2: ModelUtils.get_id()
        }

        self.opponent_model_id_dictionary = {
            0: ModelUtils.get_id(),
            1: ModelUtils.get_id(),
            2: ModelUtils.get_id()
        }

    def _go_to_point_v_wheels(
        self,
        robot_id: int,
        is_yellow: bool,
        point: 'tuple[float, float]'
    ):
        if is_yellow:
            robot = RSoccerUtils.to_robot(self.frame.robots_yellow[robot_id])
        else:
            robot = RSoccerUtils.to_robot(self.frame.robots_blue[robot_id])

        error = self._get_error(robot_id, is_yellow)

        right_speed, left_speed, current_error = MotionUtils.go_to_point(
            robot,
            point,
            error,
            self.max_motor_speed)

        self._set_error(robot_id, is_yellow, current_error)

        return left_speed, right_speed
    
    def _get_error(
        self,
        robot_id: int,
        is_yellow: bool 
    ):
        if is_yellow:
            return self.opponent_error_dictionary[robot_id]
        
        return self.own_team_error_dictionary[robot_id]
    
    def _set_error(
        self,
        robot_id: int,
        is_yellow: bool,
        error: float
    ):
        if is_yellow:
            self.opponent_error_dictionary[robot_id] = error
        else:
            self.own_team_error_dictionary[robot_id] = error
    
    def _create_ball_following_robot_command(
        self,
        behavior: RobotCurriculumBehavior
    ):
        ball = self._get_ball()
        robot_id = behavior.robot_id
        is_yellow = behavior.is_yellow

        left_speed, right_speed = self._go_to_point_v_wheels(
            robot_id,
            is_yellow,
            (ball.x, ball.y))
        
        velocity_alpha = behavior.get_velocity_alpha()

        return self._create_robot_command(
            robot_id,
            is_yellow,
            left_speed * velocity_alpha,
            right_speed * velocity_alpha)
    
    def _create_goalkeeper_ball_following_robot_command(
        self,
        behavior: RobotCurriculumBehavior
    ):
        is_yellow = behavior.is_yellow
        robot_id = behavior.robot_id

        ball = self._get_ball()
        robot = self._get_robot_by_id(robot_id, is_yellow)

        if self._is_inside_own_goal_area((ball.x, ball.y), is_yellow):
            position = (ball.x, ball.y)

            left_speed, right_speed = self._go_to_point_v_wheels(
                robot_id,
                is_yellow,
                position)
        else:
            max_y = self.get_goal_area_width() / 2
            x = self.get_field_length() / 2 - self.get_goal_area_length() / 2

            x = x if is_yellow else -x
            y = np.clip(ball.y, -max_y, max_y)

            position = x, y

            if self._is_close_to_position(robot, position):
                left_speed, right_speed = 0, 0
            else:
                left_speed, right_speed = self._go_to_point_v_wheels(
                    robot_id,
                    is_yellow,
                    position)

        velocity_alpha = behavior.get_velocity_alpha()

        return self._create_robot_command(
            robot_id,
            is_yellow,
            left_speed * velocity_alpha,
            right_speed * velocity_alpha)
    
    def _frame_to_attacker_observation(
        self,
        robot_id: int,
        is_yellow_team: bool
    ):
        return AttackerUtils.get_observation(
            self,
            robot_id,
            is_yellow_team,
            not is_yellow_team)
    
    def _frame_to_attacker_v2_observation(
        self,
        robot_id: int,
        is_yellow_team: bool
    ):
        return AttackerV2Utils.get_observation(
            self,
            robot_id,
            is_yellow_team,
            not is_yellow_team)
    
    def _frame_to_defender_observation(
        self,
        robot_id: int,
        is_yellow_team: bool
    ):
        return DefenderUtils.get_observation(
            self,
            robot_id,
            is_yellow_team,
            not is_yellow_team)
    
    def _frame_to_goalkeeper_observation(
        self,
        robot_id: int,
        is_yellow_team: bool
    ):
        return GoalkeeperUtils.get_observation(
            self,
            robot_id,
            is_yellow_team,
            not is_yellow_team)
    
    def _frame_to_observation_by_behavior(
        self,
        behavior: RobotCurriculumBehavior
    ):
        role_enum = behavior.role_enum
        robot_id = behavior.robot_id
        is_yellow_team = behavior.is_yellow

        if role_enum == RoleEnum.ATTACKER:
            return self._frame_to_attacker_observation(
                robot_id,
                is_yellow_team
            )
        elif role_enum == RoleEnum.ATTACKERV2:
            return self._frame_to_attacker_v2_observation(
                robot_id,
                is_yellow_team
            )
        elif role_enum == RoleEnum.DEFENDER:
            return self._frame_to_defender_observation(
                robot_id,
                is_yellow_team
            )
        elif role_enum == RoleEnum.GOALKEEPER:
            return self._frame_to_goalkeeper_observation(
                robot_id,
                is_yellow_team
            )
        
        return np.array([], np.float32)
    
    def _get_from_model_actions(
        self,
        behavior: RobotCurriculumBehavior
    ):
        observation = self._frame_to_observation_by_behavior(behavior)

        model = self._get_model(behavior)

        if model is None:
            return np.array([0, 0], np.float32)

        return model.predict(observation)[0]
    
    def _create_from_model_robot_command(
        self,
        behavior: RobotCurriculumBehavior
    ):
        is_yellow = behavior.is_yellow
        robot_id = behavior.robot_id

        actions = self._get_from_model_actions(behavior)

        left_speed, right_speed = self._actions_to_v_wheels(actions)
        velocity_alpha = behavior.get_velocity_alpha()

        return self._create_robot_command(
            robot_id,
            is_yellow,
            left_speed * velocity_alpha,
            right_speed * velocity_alpha)
    
    def _create_multiple_role_robot_command(
        self,
        behavior: RobotCurriculumBehavior,
        role_enum: RoleEnum
    ):
        is_yellow = behavior.is_yellow
        robot_id = behavior.robot_id
        robot = self._get_robot_by_id(robot_id, is_yellow)

        if role_enum == RoleEnum.ATTACKER:
            observation = self._frame_to_attacker_observation(robot_id, is_yellow)
            action = ModelUtils.attacker_model().predict(observation, deterministic=True)[0]
            left_speed, right_speed = self._actions_to_v_wheels(action)
        elif role_enum == RoleEnum.DEFENDER:
            observation = self._frame_to_defender_observation(robot_id, is_yellow)
            action = ModelUtils.defender_model().predict(observation, deterministic=True)[0]
            left_speed, right_speed = self._actions_to_v_wheels(action)
        elif role_enum == RoleEnum.GOALKEEPER:
            observation = self._frame_to_goalkeeper_observation(robot_id, is_yellow)
            action = ModelUtils.goalkeeper_model().predict(observation, deterministic=True)[0]
            left_speed, right_speed = self._actions_to_v_wheels(action)
        elif role_enum == RoleEnum.SUPPORTER:
            field = RSoccerUtils.get_field_by_frame(self.frame, is_yellow)
            obstacles = FieldUtils.to_obstacles_except_current_robot_and_ball(
                field,
                robot_id)

            position = get_supporter_position(
                robot_id,
                field)

            right_speed, left_speed = MotionUtils.go_to_point_univector(
                RSoccerUtils.to_robot(robot),
                position,
                obstacles)
        else:
            left_speed, right_speed = 0, 0

        return self._create_robot_command(
            robot_id,
            is_yellow,
            left_speed,
            right_speed)
    
    def _create_robot_command_by_behavior(
        self,
        behavior: RobotCurriculumBehavior,
        role_enum: 'RoleEnum | None' = None
    ):
        robot_curriculum_behavior_enum = behavior.robot_curriculum_behavior_enum

        if robot_curriculum_behavior_enum == RobotCurriculumBehaviorEnum.BALL_FOLLOWING:
            return self._create_ball_following_robot_command(behavior)
        elif robot_curriculum_behavior_enum == RobotCurriculumBehaviorEnum.GOALKEEPER_BALL_FOLLOWING:
            return self._create_goalkeeper_ball_following_robot_command(behavior)
        elif robot_curriculum_behavior_enum == RobotCurriculumBehaviorEnum.FROM_PREVIOUS_MODEL or\
            robot_curriculum_behavior_enum == RobotCurriculumBehaviorEnum.FROM_FIXED_MODEL:
            return self._create_from_model_robot_command(behavior)
        elif robot_curriculum_behavior_enum == RobotCurriculumBehaviorEnum.MULTIPLE_ROLE:
            return self._create_multiple_role_robot_command(behavior, role_enum)
        elif robot_curriculum_behavior_enum == RobotCurriculumBehaviorEnum.STRAIGHT:
            return self._create_robot_command(
            behavior.robot_id,
            behavior.is_yellow,
            30,
            30)

        return self._create_robot_command(
            behavior.robot_id,
            behavior.is_yellow,
            0,
            0)

    def _get_velocity_factor(self):
        rsoccer_max_motor_speed = self.max_v / self.field.rbt_wheel_radius
        return self.max_motor_speed / rsoccer_max_motor_speed

    def _actions_to_v_wheels(
        self,
        actions: np.ndarray
    ):
        left_wheel_speed = actions[0] * self.max_v
        right_wheel_speed = actions[1] * self.max_v

        left_wheel_speed, right_wheel_speed = np.clip(
            (left_wheel_speed, right_wheel_speed),
            -self.max_v,
            self.max_v)

        factor = self._get_velocity_factor()

        left_wheel_speed *= factor
        right_wheel_speed *= factor

        if abs(left_wheel_speed) < self.v_wheel_deadzone:
            left_wheel_speed = 0

        if abs(right_wheel_speed) < self.v_wheel_deadzone:
            right_wheel_speed = 0

        left_wheel_speed /= self.field.rbt_wheel_radius
        right_wheel_speed /= self.field.rbt_wheel_radius

        return left_wheel_speed, right_wheel_speed
    
    def _get_commands(self, action):
        commands = []

        v_wheel0, v_wheel1 = self._actions_to_v_wheels(action)

        robot = self._create_robot_command(
            self.robot_id,
            False,
            v_wheel0,
            v_wheel1)

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
                theta1 = theta()
            else:
                position_function = self.get_position_function_by_behavior(behavior, ball_position)
                position = get_position(position_function)
                theta1 = 180

            frame.robots_yellow[i] = Robot(
                x=position[0],
                y=position[1],
                theta=theta1)

        return frame

    def set_task(self, task: CurriculumTask):
        self.task = task

    def _get_model(
        self,
        behavior: RobotCurriculumBehavior
    ):
        if behavior.is_yellow:
            model_id = self.opponent_model_id_dictionary[behavior.robot_id]
        else:
            model_id = self.own_team_model_id_dictionary[behavior.robot_id]

        return ModelUtils.get_model(model_id, behavior.model_path)
