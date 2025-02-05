import random
import numpy as np
from gymnasium.spaces import Box

from rsoccer_gym.Entities import Frame, Robot, Ball
from lib.domain.enums.foul_enum import FoulEnum
from lib.environment.base_environment import BaseEnvironment

from configuration.configuration import Configuration
from lib.utils.configuration_utils import ConfigurationUtils
from lib.utils.field_utils import FieldUtils

TRAINING_EPISODE_DURATION = Configuration.rsoccer_training_episode_duration

NUMBER_ROBOTS_BLUE = Configuration.rsoccer_team_blue_number_robots
NUMBER_ROBOTS_YELLOW = Configuration.rsoccer_team_yellow_number_robots

V_WHEEL_DEADZONE = Configuration.rsoccer_robot_speed_dead_zone_meters_seconds

TIME_STEP = Configuration.rsoccer_training_time_step

# addapt this for your robot
MAX_MOTOR_SPEED = Configuration.firasim_robot_speed_max_radians_seconds

class EvaluationEnvironment(BaseEnvironment):
    def __init__(
        self,
        render_mode="rgb_array"
    ):
        super().__init__(
            field_type=0,
            n_robots_blue=NUMBER_ROBOTS_BLUE,
            n_robots_yellow=NUMBER_ROBOTS_YELLOW,
            time_step=TIME_STEP,
            robot_id=0,
            training_episode_duration=TRAINING_EPISODE_DURATION,
            render_mode=render_mode)

        self.max_motor_speed = MAX_MOTOR_SPEED
        self.v_wheel_deadzone = V_WHEEL_DEADZONE

        self.action_space = Box(
            low=-1,
            high=1,
            shape=(1,),
            dtype=np.float32)

        self.observation_space = Box(
            low=-1,
            high=1,
            shape=(1,),
            dtype=np.float32)
        
        self.ball_stucked_time = None
        self.stucked_ball_time = 10
        self.ball_min_speed_for_stuck = 0.1
        self.foul_enum = FoulEnum.KICKOFF
        self.quadrant = 1
        
    def reset(
        self,
        *,
        seed=None,
        options=None
    ):
        self.ball_stucked_time = None
        self.foul_enum = FoulEnum.KICKOFF
        return super().reset(seed=seed, options=options)
        
    def _is_done(self):
        return False
    
    def try_set_ball_stucked_time(self):
        ball = self._get_ball()
        speed = np.sqrt(ball.v_x ** 2 + ball.v_y ** 2)
        
        if self.ball_stucked_time is None and\
                speed <= self.ball_min_speed_for_stuck:
            self.ball_stucked_time = self._get_episode_elapsed_time()
            self.quadrant = FieldUtils.get_quadrant((ball.x, ball.y))
        elif speed > self.ball_min_speed_for_stuck:
            self.ball_stucked_time = None

    def is_ball_stucked(self):
        return self.ball_stucked_time is not None and\
            self._get_episode_elapsed_time() - self.ball_stucked_time >= self.stucked_ball_time
        
    def _frame_to_observations(self):
        return np.array([0], dtype=np.float32)
    
    def _calculate_reward_and_done(self):
        self.try_set_ball_stucked_time()
        return 0, self._is_done()

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

        for i in range(self.n_robots_blue):
            index = 2 * i
            v_wheel0, v_wheel1 = self._actions_to_v_wheels(action[index:index+2])
            robot = self._create_robot_command(
                i,
                False,
                v_wheel0,
                v_wheel1)

            commands.append(robot)

        for i in range(self.n_robots_yellow):
            index = 6 + 2 * i
            v_wheel0, v_wheel1 = self._actions_to_v_wheels(action[index:index+2])
            robot = self._create_robot_command(
                i,
                True,
                v_wheel0,
                v_wheel1)

            commands.append(robot)

        return commands
    
    def _convert_positionings_to_right_team(self, positionings):
        for i in range(len(positionings)):
            positionings[i] = (-positionings[i][0], -positionings[i][1])

    def _get_position_tuple(self, position):
        teste = []
        for i in position.keys():
            if i == "ball":
                continue

            teste.append((position[i]["x"], position[i]["y"]))

        return teste
    
    def _get_right_team_quadrant(self):
        if self.quadrant == 1:
            return 3
        elif self.quadrant == 2:
            return 4
        elif self.quadrant == 3:
            return 1
        return 2

    def _get_initial_positions_frame(self):
        frame: Frame = Frame()
        
        if self.foul_enum == FoulEnum.FREE_BALL:
            team_positions_dict = ConfigurationUtils.get_game_states_free_ball_team_positionings(self.quadrant)
            team_positions = self._get_position_tuple(team_positions_dict)

            foe_team_positions_dict = ConfigurationUtils.get_game_states_free_ball_team_positionings(
                self._get_right_team_quadrant()
            )

            foe_team_positions = self._get_position_tuple(foe_team_positions_dict)
            self._convert_positionings_to_right_team(foe_team_positions)

            ball_position = team_positions_dict["ball"]["x"], team_positions_dict["ball"]["y"]
        else:
            team_positions_dict = ConfigurationUtils.get_game_states_kickoff_team_positionings()
            team_positions = self._get_position_tuple(team_positions_dict)

            foe_team_positions_dict = ConfigurationUtils.get_game_states_kickoff_foe_team_positionings()
            foe_team_positions = self._get_position_tuple(foe_team_positions_dict)
            self._convert_positionings_to_right_team(foe_team_positions)

            ball_position = (0, 0)

        blue_team_positions = team_positions
        yellow_team_positions = foe_team_positions

        frame.ball = Ball(x=ball_position[0], y=ball_position[1])

        for i in range(self.n_robots_blue):
            position = blue_team_positions[i]
            frame.robots_blue[i] = Robot(
                x=position[0],
                y=position[1],
                theta=0)

        for i in range(self.n_robots_yellow):
            position = yellow_team_positions[i]
            frame.robots_yellow[i] = Robot(
                x=position[0],
                y=position[1],
                theta=180)

        return frame
