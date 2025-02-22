from typing import List

import gymnasium as gym
import numpy as np
import pygame

from rsoccer_gym.Entities import Frame, Robot
from rsoccer_gym.Render import COLORS, VSSRenderField, VSSRobot, Ball
from rsoccer_gym.Simulators.rsim import RSimVSS
from rsoccer_gym.Utils import KDTree

from lib.domain.field import Field
from lib.utils.geometry_utils import GeometryUtils
from lib.utils.field_utils import FieldUtils
from lib.utils.rsoccer.rsoccer_utils import RSoccerUtils

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
        training_episode_duration: int,
        render_mode="human",
    ):
        super().__init__()
        self.render_mode = render_mode
        self.time_step = time_step
        self.robot_id = robot_id
        self.training_episode_duration = training_episode_duration

        self.rsim = RSimVSS(
            field_type=field_type,
            n_robots_blue=n_robots_blue,
            n_robots_yellow=n_robots_yellow,
            time_step_ms=int(self.time_step * 1000),
        )

        self.n_robots_blue = n_robots_blue
        self.n_robots_yellow = n_robots_yellow

        self.field_type = field_type
        self.field_params = self.rsim.get_field_params()
        max_wheel_rad_s = (self.field_params.rbt_motor_max_rpm / 60) * 2 * np.pi
        self.max_v = max_wheel_rad_s * self.field_params.rbt_wheel_radius

        # 0.04 = robot radius (0.0375) + wheel thicknees (0.0025)
        self.max_w = np.rad2deg(self.max_v / 0.04)

        self.frame: Frame = None
        self.last_frame: Frame = None

        self.rendering_frame: Frame = None

        self.steps = 0
        self.sent_commands = None

        self.field_renderer = VSSRenderField()
        self.window_surface = None
        self.window_size = self.field_renderer.window_size
        self.clock = None

        self.field = Field()
        self.opponent_field = Field()

    def step(self, action):
        self.steps += 1
        commands: List[Robot] = self._get_commands(action)
        self.rsim.send_commands(commands)
        self.sent_commands = commands

        self.last_frame = self.frame

        self.rendering_frame = self._get_rendering_frame_from_rsim()
        self.frame = RSoccerUtils._get_frame_by_rendering_frame(self.rendering_frame)

        RSoccerUtils.set_field_by_frame(self.field, self.frame, False)
        RSoccerUtils.set_field_by_frame(self.opponent_field, self.frame, True)

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

        initial_pos_frame = RSoccerUtils._get_rendering_frame_by_frame(
            self._get_initial_positions_frame()
        )

        self.rsim.reset(initial_pos_frame)

        self.rendering_frame = self._get_rendering_frame_from_rsim()
        self.frame = RSoccerUtils._get_frame_by_rendering_frame(self.rendering_frame)

        RSoccerUtils.set_field_by_frame(self.field, self.frame, False)
        RSoccerUtils.set_field_by_frame(self.opponent_field, self.frame, True)

        obs = self._frame_to_observations()

        if self.render_mode == "human":
            self.render()

        return obs, {}
    
    def _get_rendering_frame_from_rsim(self):
        rendering_frame = self.rsim.get_frame()

        for item in rendering_frame.robots_blue:
            rendering_frame.robots_blue[item].yellow = False

        for item in rendering_frame.robots_yellow:
            rendering_frame.robots_yellow[item].yellow = True

        return rendering_frame

    def _render(self):
        def pos_transform(pos_x, pos_y):
            return (
                int(pos_x * self.field_renderer.scale + self.field_renderer.center_x),
                int(pos_y * self.field_renderer.scale + self.field_renderer.center_y),
            )

        ball = Ball(
            *pos_transform(self.rendering_frame.ball.x, self.rendering_frame.ball.y),
            self.field_renderer.scale
        )

        self.field_renderer.draw(self.window_surface)

        for i in range(self.n_robots_blue):
            robot = self.rendering_frame.robots_blue[i]
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
            robot = self.rendering_frame.robots_yellow[i]
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
    
    def _get_episode_elapsed_time(self):
        return int(self.steps * self.time_step)
    
    def _get_time_factor(self):
        return self._get_episode_elapsed_time() / self.training_episode_duration
    
    def _has_episode_time_exceeded(self):
        elapsed_time = self._get_episode_elapsed_time()

        if elapsed_time == 0:
            return False

        return elapsed_time % self.training_episode_duration == 0

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
        return self.field_params.length

    def get_field_width(self):
        return self.field_params.width

    def get_goal_area_length(self):
        return self.field_params.penalty_length

    def get_goal_area_width(self):
        return self.field_params.penalty_width

    def get_goal_depth(self):
        return self.field_params.goal_depth
    
    def get_goal_width(self):
        return self.field_params.goal_width

    def get_inside_own_goal_position(self, is_yellow_team: bool):
        return FieldUtils.get_inside_own_goal_position(
            self.get_field_length(),
            self.get_goal_depth(),
            not is_yellow_team)

    def _get_ball(self):
        return self.frame.ball

    def get_ball_radius(self):
        return self.field_params.ball_radius

    def get_robot_radius(self):
        return self.field_params.rbt_radius

    def get_frame(self):
        return self.frame
    
    def _ball_gradient_reward_by_positions(
        self,
        previous_ball_potential: 'float | None',
        desired_position: float,
        undesired_position: float
    ):
        field_length = self.get_field_length()
        ball = self._get_ball()

        distance_to_desired = GeometryUtils.distance(
            (ball.x, ball.y),
            desired_position)

        distance_to_undesired = GeometryUtils.distance(
            (ball.x, ball.y),
            undesired_position)

        ball_potential = ((distance_to_undesired - distance_to_desired) / field_length - 1) / 2

        if previous_ball_potential is not None:
            ball_potential_difference = ball_potential - previous_ball_potential
            reward = np.clip(
                ball_potential_difference * 3 / self.time_step,
                -5.0,
                5.0)
        else:
            reward = 0

        return reward, ball_potential
    
    def _move_reward(
        self,
        position: 'tuple[float, float]',
        robot_id: int = 0,
        min_value: float = -5.0,
        max_value: float = 5.0
    ):
        robot = self._get_team_robot(robot_id)
        robot_position = np.array([robot.x, robot.y])

        robot_velocities = np.array([robot.v_x, robot.v_y])
        robot_target_vector = np.array(position) - robot_position
        robot_target_vector = robot_target_vector / np.linalg.norm(robot_target_vector)

        move_reward = np.dot(robot_target_vector, robot_velocities)

        return np.clip(move_reward / 0.4, min_value, max_value)

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

    def _is_inside_field(
        self,
        position: 'tuple[float, float]'
    ):
        return FieldUtils.is_inside_field(
            position[0],
            position[1],
            self.get_field_length(),
            self.get_field_width(),
            self.get_goal_width(),
            self.get_goal_depth())
    
    def _is_inside_playable_field(
        self,
        position: 'tuple[float, float]'
    ):
        return FieldUtils.is_inside_playable_field(
            position[0],
            position[1],
            self.get_field_length(),
            self.get_field_width())
    
    def _is_close_to_wall(
        self,
        position: 'tuple[float, float]',
        tolerance: float = 0.1
    ):
        return FieldUtils.is_close_to_wall(
            position,
            self.get_field_length(),
            self.get_field_width(),
            tolerance)

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
    
    def _get_team_robot(self, robot_id: int):
        return self.frame.robots_blue[robot_id]

    def _create_robot_command(
        self,
        id: int,
        is_yellow_robot: bool,
        left_speed: float,
        right_speed: float
    ):
        return Robot(
            yellow=is_yellow_robot,
            id=id,
            v_wheel0=right_speed,
            v_wheel1=left_speed)

    def _get_yellow_robot_by_id(self, id: int):
        return self.frame.robots_yellow[id]

    def _get_blue_robot_by_id(self, id: int):
        return self.frame.robots_blue[id]

    def _get_robot_by_id(self, id: int, is_yellow: bool):
        if is_yellow:
            return self._get_yellow_robot_by_id(id)

        return self._get_blue_robot_by_id(id)
    
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
