from typing import List

import gymnasium as gym
import numpy as np
import pygame
import random

from rsoccer_gym.Entities import Frame, Robot
from rsoccer_gym.Render import COLORS, Ball, VSSRenderField, VSSRobot
from rsoccer_gym.Simulators.rsim import RSimVSS
from rsoccer_gym.Utils import KDTree

from lib.utils.geometry_utils import GeometryUtils
from lib.utils.field_utils import FieldUtils

class BaseEnvironment(gym.Env):
    metadata = {
        "render.modes": ["human", "rgb_array"],
        "render_modes": ["human", "rgb_array"],
        "render_fps": 60,
        "render.fps": 60,
    }

    def __init__(
        self,
        field_type: int,
        n_robots_blue: int,
        n_robots_yellow: int,
        time_step: float,
        robot_id: int,
        render_mode="human",
    ):
        # Initialize Simulator
        super().__init__()
        self.render_mode = render_mode
        self.time_step = time_step
        self.robot_id = robot_id

        self.rsim = RSimVSS(
            field_type=field_type,
            n_robots_blue=n_robots_blue,
            n_robots_yellow=n_robots_yellow,
            time_step_ms=int(self.time_step * 1000),
        )

        self.n_robots_blue = n_robots_blue
        self.n_robots_yellow = n_robots_yellow

        self.field_type = field_type
        self.field = self.rsim.get_field_params()
        max_wheel_rad_s = (self.field.rbt_motor_max_rpm / 60) * 2 * np.pi
        self.max_v = max_wheel_rad_s * self.field.rbt_wheel_radius

        # 0.04 = robot radius (0.0375) + wheel thicknees (0.0025)
        self.max_w = np.rad2deg(self.max_v / 0.04)

        self.frame: Frame = None
        self.last_frame: Frame = None
        self.steps = 0
        self.sent_commands = None

        self.field_renderer = VSSRenderField()
        self.window_surface = None
        self.window_size = self.field_renderer.window_size
        self.clock = None

    def step(self, action):
        self.steps += 1
        commands: List[Robot] = self._get_commands(action)
        self.rsim.send_commands(commands)
        self.sent_commands = commands

        self.last_frame = self.frame
        self.frame = self._get_rsim_frame()

        observation = self._frame_to_observations()
        reward, done = self._calculate_reward_and_done()

        if self.render_mode == "human":
            self.render()

        return observation, reward, done, False, {}

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed, options=options)
        self.steps = 0
        self.last_frame = None
        self.sent_commands = None

        initial_pos_frame: Frame = self._get_initial_positions_frame()
        self.rsim.reset(initial_pos_frame)

        self.frame = self._get_rsim_frame()
        obs = self._frame_to_observations()

        if self.render_mode == "human":
            self.render()

        return obs, {}
    
    def _get_rsim_frame(self):
        frame = self.rsim.get_frame()

        for item in frame.robots_blue:
            frame.robots_blue[item].yellow = False

        for item in frame.robots_yellow:
            frame.robots_yellow[item].yellow = True

        return frame

    def _render(self):
        def pos_transform(pos_x, pos_y):
            return (
                int(pos_x * self.field_renderer.scale + self.field_renderer.center_x),
                int(pos_y * self.field_renderer.scale + self.field_renderer.center_y),
            )

        ball = Ball(
            *pos_transform(self.frame.ball.x, self.frame.ball.y),
            self.field_renderer.scale
        )

        self.field_renderer.draw(self.window_surface)

        for i in range(self.n_robots_blue):
            robot = self.frame.robots_blue[i]
            x, y = pos_transform(robot.x, robot.y)
            rbt = VSSRobot(
                x,
                y,
                robot.theta,
                self.field_renderer.scale,
                robot.id,
                COLORS["BLUE"],
            )
            rbt.draw(self.window_surface)

        for i in range(self.n_robots_yellow):
            robot = self.frame.robots_yellow[i]
            x, y = pos_transform(robot.x, robot.y)
            rbt = VSSRobot(
                x,
                y,
                robot.theta,
                self.field_renderer.scale,
                robot.id,
                COLORS["YELLOW"],
            )
            rbt.draw(self.window_surface)
        ball.draw(self.window_surface)

    def render(self) -> None:
        """
        Renders the game depending on
        ball's and players' positions.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """

        if self.window_surface is None:
            pygame.init()

            if self.render_mode == "human":
                pygame.display.init()
                pygame.display.set_caption("VSSS Environment")
                self.window_surface = pygame.display.set_mode(self.window_size)
            elif self.render_mode == "rgb_array":
                self.window_surface = pygame.Surface(self.window_size)

        assert (
            self.window_surface is not None
        ), "Something went wrong with pygame. This should never happen."

        if self.clock is None:
            self.clock = pygame.time.Clock()
        self._render()
        if self.render_mode == "human":
            pygame.event.pump()
            pygame.display.update()
            self.clock.tick(self.metadata["render_fps"])
        elif self.render_mode == "rgb_array":
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(self.window_surface)), axes=(1, 0, 2)
            )

    def close(self):
        if self.window_surface is not None:
            import pygame

            pygame.display.quit()
            pygame.quit()
        self.rsim.stop()

    def _get_commands(self, action):
        """returns a list of commands of type List[Robot] from type action_space action"""
        raise NotImplementedError

    def _frame_to_observations(self):
        """returns a type observation_space observation from a type List[Robot] state"""
        raise NotImplementedError

    def _calculate_reward_and_done(self):
        """returns reward value and done flag from type List[Robot] state"""
        raise NotImplementedError

    def _get_initial_positions_frame(self) -> Frame:
        """returns frame with robots initial positions"""
        raise NotImplementedError

    def norm_v(self, v):
        return np.clip(v / self.max_v, -1, 1)

    def norm_w(self, w):
        return np.clip(w / self.max_w, -1, 1)

    def norm_x(self, x):
        return np.clip(x / self.get_max_x(), -1, 1)

    def norm_y(self, y):
        return np.clip(y / self.get_max_y(), -1, 1)

    def get_max_x(self):
        return self.get_field_length() / 2 + self.get_goal_depth()

    def get_max_y(self):
        return self.get_field_width() / 2

    def get_field_length(self):
        return self.field.length

    def get_field_width(self):
        return self.field.width

    def get_goal_area_length(self):
        return self.field.penalty_length

    def get_goal_area_width(self):
        return self.field.penalty_width

    def get_goal_depth(self):
        return self.field.goal_depth
    
    def get_goal_width(self):
        return self.field.goal_width

    def get_inside_own_goal_position(self, is_yellow_team: bool):
        return FieldUtils.get_inside_own_goal_position(
            self.get_field_length(),
            self.get_goal_depth(),
            not is_yellow_team)

    def _get_ball(self):
        return self.frame.ball

    def get_ball_radius(self):
        return self.field.ball_radius

    def get_robot_radius(self):
        return self.field.rbt_radius

    def get_frame(self):
        return self.frame

    @staticmethod
    def get_position(places: KDTree, min_distance, get_position_fn):
        position = get_position_fn()

        while places.get_nearest(position)[1] < min_distance:
            position = get_position_fn()

        places.insert(position)

        return position

    def _get_random_position_inside_field(self):
        return FieldUtils.get_random_position_inside_field(
            self.get_field_length(),
            self.get_field_width())

    def _get_random_position_inside_own_goal_area(self):
        return FieldUtils.get_random_position_inside_own_goal_area(
            self.get_field_length(),
            self.get_goal_area_length(),
            self.get_goal_area_width(),
            True)

    def _get_random_position_inside_opponent_goal_area(self):
        return FieldUtils.get_random_position_inside_own_goal_area(
            self.get_field_length(),
            self.get_goal_area_length(),
            self.get_goal_area_width(),
            False)

    def _get_random_position_inside_own_area(self):
        return FieldUtils.get_random_position_inside_own_area(
            self.get_field_length(),
            self.get_field_width(),
            True)

    def _get_random_position_inside_opponent_area(self):
        return FieldUtils.get_random_position_inside_own_area(
            self.get_field_length(),
            self.get_field_width(),
            False)

    def _get_own_goal_position(self):
        return FieldUtils.get_own_goal_position(
            self.get_field_length(),
            True)

    def _get_opponent_goal_position(self):
        return FieldUtils.get_own_goal_position(
            self.get_field_length(),
            False)

    def _get_random_position_at_distance(
        self,
        distance: float,
        position: 'tuple[float, float]'
    ):
        return FieldUtils.get_random_position_at_distance(
            self.get_field_length(),
            self.get_field_width(),
            position,
            distance)

    def _get_random_position_inside_own_area_except_goal_area(self):
        return FieldUtils.get_random_position_inside_own_area_except_goal_area(
            self.get_field_length(),
            self.get_field_width(),
            self.get_goal_area_length(),
            self.get_goal_area_width(),
            True)

    def _get_random_position_inside_opponent_area_except_goal_area(self):
        return FieldUtils.get_random_position_inside_own_area_except_goal_area(
            self.get_field_length(),
            self.get_field_width(),
            self.get_goal_area_length(),
            self.get_goal_area_width(),
            False)

    def _is_inside_field(
        self,
        position: 'tuple[float, float]'
    ):
        return FieldUtils.is_inside_field(
            position[0],
            position[1],
            self.get_field_length(),
            self.get_field_width())

    def _is_inside_own_goal_area(
        self,
        position: 'tuple[float, float]',
        is_yellow_team: bool
    ):
        return FieldUtils.is_inside_own_goal_area(
            position,
            self.get_field_length(),
            self.get_goal_area_length(),
            self.get_goal_area_width(),
            not is_yellow_team)

    def _get_max_distance(self):
        max_x = self.get_max_x() - self.get_goal_depth()
        max_y = self.get_max_y()

        return GeometryUtils.distance(
            (-max_x, max_y),
            (max_x, -max_y))

    def _energy_penalty(self):
        en_penalty_1 = abs(self.sent_commands[0].v_wheel0)
        en_penalty_2 = abs(self.sent_commands[0].v_wheel1)
        return - (en_penalty_1 + en_penalty_2)

    def _any_team_scored_goal(self):
        ball = self._get_ball()
        return abs(ball.x) > (self.get_field_length() / 2)

    def _has_received_goal(self):
        ball = self._get_ball()
        return ball.x < -self.get_field_length() / 2

    def _has_scored_goal(self):
        if not self._any_team_scored_goal():
            return None
        return not self._has_received_goal()

    def _get_agent(self):
        return self.frame.robots_blue[self.robot_id]

    def _create_robot_command(
        self,
        id: int,
        is_yellow_robot: bool,
        v_wheel_0: float,
        v_wheel_1: float
    ):
        return Robot(
            yellow=is_yellow_robot,
            id=id,
            v_wheel0=v_wheel_0,
            v_wheel1=v_wheel_1)

    def _get_yellow_robot_by_id(self, id: int):
        return self.frame.robots_yellow[id]

    def _get_blue_robot_by_id(self, id: int):
        return self.frame.robots_blue[id]

    def _get_robot_by_id(self, id: int, is_yellow: bool):
        if is_yellow:
            return self._get_yellow_robot_by_id(id)

        return self._get_blue_robot_by_id(id)
    
    def _get_own_area_position_function(self, is_yellow: bool):
        if is_yellow:
            return self._get_random_position_inside_opponent_area

        return self._get_random_position_inside_own_area

    def _get_opponent_area_position_function(self, is_yellow: bool):
        return self._get_own_area_position_function(not is_yellow)

    def _get_goal_area_position_function(self, is_yellow: bool):
        if is_yellow:
            return self._get_random_position_inside_opponent_goal_area

        return self._get_random_position_inside_own_goal_area

    def _get_opponent_goal_area_position_function(self, is_yellow: bool):
        return self._get_goal_area_position_function(not is_yellow)

    def _get_own_area_except_goal_area_position_function(self, is_yellow: bool):
        if is_yellow:
            return self._get_random_position_inside_opponent_area_except_goal_area

        return self._get_random_position_inside_own_area_except_goal_area

    def _get_opponent_area_except_goal_area_position_function(self, is_yellow: bool):
        return self._get_own_area_except_goal_area_position_function(not is_yellow)

    def _get_relative_to_own_goal_position_function(self, is_yellow: bool, distance: float):
        if not is_yellow:
            return lambda: self._get_random_position_at_distance(
                distance,
                self._get_own_goal_position())

        return lambda: self._get_random_position_at_distance(
            distance,
            self._get_opponent_goal_position())

    def _get_relative_to_opponent_goal_position_function(self, is_yellow: bool, distance: float):
        return self._get_relative_to_own_goal_position_function(not is_yellow, distance)

    def _get_random_position_at_distance_position_function(
        self,
        distance: float,
        position: 'tuple[float, float]'
    ):
        return lambda: self._get_random_position_at_distance(distance, position)
    
    def _get_position_close_to_wall_relative_to_own_goal_function(
        self,
        distance: float,
        distance_to_wall: float,
        is_yellow_team: bool
    ):
        return lambda: self._get_position_close_to_wall_relative_to_goal(
            distance,
            distance_to_wall,
            not is_yellow_team)
    
    def _get_position_close_to_wall_relative_to_opponent_goal_function(
        self,
        distance: float,
        distance_to_wall: float,
        is_yellow_team: bool
    ):
        return lambda: self._get_position_close_to_wall_relative_to_goal(
            distance,
            distance_to_wall,
            is_yellow_team)
    
    def _get_position_close_to_wall_relative_to_goal(
        self,
        distance: float,
        distance_to_wall: float,
        is_left_team: bool
    ):
        upper = random.choice([True, False])

        return FieldUtils.get_position_close_to_wall_relative_to_own_goal(
            self.get_field_length(),
            self.get_field_width(),
            self.get_goal_width(),
            distance,
            distance_to_wall,
            is_left_team,
            upper)
    
    def _get_random_position_at_distance_to_vertical_line(
        self,
        distance: float,
        x_line: float,
        y_range: 'tuple[float, float]',
        left_to_line: bool,
        is_left_team: bool
    ):
        return FieldUtils.get_random_position_at_distance_to_vertical_line(
            distance,
            x_line,
            y_range,
            left_to_line,
            is_left_team)
    
    def _get_random_position_at_distance_to_own_vertical_line_function(
        self,
        distance: float,
        x_line: float,
        y_range: 'tuple[float, float]',
        left_to_line: bool,
        is_yellow_team: bool
    ):
        return lambda: self._get_random_position_at_distance_to_vertical_line(
            distance,
            x_line,
            y_range,
            left_to_line,
            not is_yellow_team)
    
    def _get_random_position_at_distance_to_opponent_vertical_line_function(
        self,
        distance: float,
        x_line: float,
        y_range: 'tuple[float, float]',
        left_to_line: bool,
        is_yellow_team: bool
    ):
        return lambda: self._get_random_position_at_distance_to_vertical_line(
            distance,
            x_line,
            y_range,
            left_to_line,
            is_yellow_team)
    
    def _get_position_behind_position_function(
        self,
        position: 'tuple[float, float]',
        distance: float,
        is_yellow_team: bool
    ):
        return lambda: self._get_position_behind_position(
            position,
            distance,
            not is_yellow_team)
    
    def _get_position_behind_position(
        self,
        position: 'tuple[float, float]',
        distance: float,
        is_left_team: bool
    ):
        if not is_left_team:
            distance = -distance

        x = position[0] - distance
        y = position[1]
        
        return x, y
    
    def _is_close_to_ball(
        self,
        tolerance: float = 0.1
    ):
        ball = self._get_ball()
        robot = self._get_agent()

        return GeometryUtils.is_close(
            (robot.x, robot.y),
            (ball.x, ball.y),
            tolerance)
    
    def _is_close_to_position(
        self,
        robot: Robot,
        position: 'tuple[float, float]',
        tolerance: float = 0.1
    ):
        return GeometryUtils.is_close(
            (robot.x, robot.y),
            position,
            tolerance)
    
    def _is_outside_field(
        self,
        position: 'tuple[float, float]'
    ):
        return not self._is_inside_field(position)
