import numpy as np

from gymnasium.spaces import Box
from rsoccer_gym.Entities import Robot

from lib.domain.curriculum_task import CurriculumTask
from lib.environment.base_curriculum_environment import BaseCurriculumEnvironment
from lib.utils.geometry_utils import GeometryUtils
from lib.utils.rsoccer.rsoccer_utils import RSoccerUtils

class DefenderEnvironment(BaseCurriculumEnvironment):
    def __init__(
        self,
        task: CurriculumTask,
        render_mode="rgb_array"
    ):
        super().__init__(
            task=task,
            render_mode=render_mode,
            robot_id=0)

        self.action_space = Box(
            low=-1,
            high=1,
            shape=(2,),
            dtype=np.float32)

        self.observation_space = Box(
            low=-1,
            high=1,
            shape=(34,),
            dtype=np.float32)

        self.defensive_line_x = 0
        self.distance_when_last_robot_touched_ball_defensive_area = None
        self.threshold_ball = .07
        self.is_yellow_team = False

    def reset(
        self,
        *,
        seed=None,
        options=None
    ):
        self.distance_when_last_robot_touched_ball_defensive_area = None
        return super().reset(seed=seed, options=options)

    def _is_done(self):
        if self._any_team_scored_goal():
            return True
        elif self._is_ball_cleared_from_defense_area():
            return True
        elif self._has_episode_time_exceeded():
            return True
        return False

    def _frame_to_observations(self):
        observation = []

        current_robot = self._get_robot_by_id(self.robot_id, self.is_yellow_team)
        ball = self._get_ball()

        def extend_observation_by_ball():
            observation.extend([
                self.norm_x(ball.x),
                self.norm_y(ball.y),
                self.norm_v(ball.v_x),
                self.norm_v(ball.v_y)
            ])

        def extend_observation_by_robot(robot: Robot):
            theta = RSoccerUtils.get_corrected_angle(current_robot.theta) / np.pi

            if self._is_inside_field((robot.x, robot.y)): 
                observation.extend([
                    self.norm_x(robot.x),
                    self.norm_y(robot.y),
                    theta,
                    self.norm_v(robot.v_x),
                    self.norm_v(robot.v_y)
                ])
            else:
                observation.extend([0, 0, 0, 0, 0])

        extend_observation_by_ball()

        frame = self.frame

        for i in range(self.n_robots_blue):
            extend_observation_by_robot(frame.robots_blue[i])

        for i in range(self.n_robots_yellow):
            extend_observation_by_robot(frame.robots_yellow[i])

        return np.array(observation, dtype=np.float32)

    def _move_towards_ball_reward(self):
        ball = self._get_ball()
        return self._move_reward((ball.x, ball.y))
    
    def _get_max_distance_to_defensive_line(self):
        goal_position = self._get_own_goal_position()
        return abs(goal_position[0] - self.defensive_line_x)

    def _calculate_reward_and_done(self):
        self._try_set_distance_when_last_robot_touched_ball_defensive_area()

        reward = self._get_reward()
        is_done = self._is_done()

        if is_done:
            if self._any_team_scored_goal() and self._has_received_goal():
                reward = -10
                self.last_game_score = -1
            elif self._is_ball_cleared_from_defense_area():
                factor = self.distance_when_last_robot_touched_ball_defensive_area /\
                    self._get_max_distance_to_defensive_line()
                
                reward = 10 * factor
                self.last_game_score = 1
            elif self._is_ball_inside_defensive_area():
                reward = -5
                self.last_game_score = -.5
            else:
                self.last_game_score = 0

        return reward, is_done
    
    def _are_two_team_robots_inside_goal_area_with_ball(self):
        number_robots_inside_goal_area = 0

        if not self._is_ball_inside_goal_area():
            return False

        for item in self.frame.robots_blue:
            robot = self.frame.robots_blue[item]

            if self._is_inside_own_goal_area(
                (robot.x, robot.y),
                self.is_yellow_team
            ):
                number_robots_inside_goal_area += 1

        return number_robots_inside_goal_area >= 2

    def _get_reward(self):
        w_move = 0.2
        w_ball_gradient = 0.8
        w_energy = 2e-4

        energy_penalty = self._energy_penalty()

        if self._is_ball_inside_defensive_area():
            gradient_ball_potential, ball_gradient = \
                self._get_ball_gradient_towards_defensive_line_reward()

            self.previous_ball_potential = ball_gradient
            move_reward = self._move_towards_ball_reward()

            reward = w_move * move_reward + \
                w_ball_gradient * gradient_ball_potential + \
                w_energy * energy_penalty
        else:
            move_reward = self._get_positioning_move_reward()

            reward = w_move * move_reward + \
                w_energy * energy_penalty

        return reward

    def _get_ball_gradient_towards_defensive_line_reward(self):
        ball = self._get_ball()
        own_goal_position = self.get_inside_own_goal_position(self.is_yellow_team)
        defensive_line_position = (self.defensive_line_x, ball.y)

        return self._ball_gradient_reward_by_positions(
            self.previous_ball_potential,
            own_goal_position,
            defensive_line_position)
    
    def _is_ball_cleared_from_defense_area(self):
        return not self._is_ball_inside_defensive_area() and\
            self.distance_when_last_robot_touched_ball_defensive_area is not None

    def _is_ball_inside_defensive_area(self):
        return self._get_ball().x <= self.defensive_line_x

    def _is_ball_inside_goal_area(self):
        ball = self._get_ball()
        return self._is_inside_own_goal_area(
            (ball.x, ball.y),
            self.is_yellow_team)

    def _is_agent_inside_defensive_area(self):
        return self._get_agent().x <= self.defensive_line_x

    def _try_set_distance_when_last_robot_touched_ball_defensive_area(self):
        if not self._is_ball_inside_defensive_area():
            return

        robot_touched_ball_defensive_area = self._get_robot_touched_ball()

        if robot_touched_ball_defensive_area is None:
            return
        
        ball = self._get_ball()
        robot = self._get_agent()

        if robot_touched_ball_defensive_area.id == robot.id and\
                robot_touched_ball_defensive_area.yellow == robot.yellow:
            if self.distance_when_last_robot_touched_ball_defensive_area is None:
                self.distance_when_last_robot_touched_ball_defensive_area =\
                    abs(self.defensive_line_x - ball.x)
        else:
            self.distance_when_last_robot_touched_ball_defensive_area = None

    def _get_robot_touched_ball(self):
        ball = self._get_ball()

        minimum_distance = None
        robot_touched_ball_defensive_area = None

        def distance_to_ball(robot: Robot):
            return GeometryUtils.distance(
                (robot.x, robot.y),
                (ball.x, ball.y))
        
        for item in self.task.behaviors:
            robot = self._get_robot_by_id(item.robot_id, item.is_yellow)
            distance = distance_to_ball(robot)

            if distance < self.threshold_ball and\
                    (minimum_distance is None or distance < minimum_distance):
                robot_touched_ball_defensive_area = robot
                minimum_distance = distance

        return robot_touched_ball_defensive_area

    def _get_positioning_move_reward(self):
        ball = self._get_ball()
        robot = self._get_agent()
        length = self.get_field_length()

        position1 = (-length / 2, ball.y)
        position2 = (0, ball.y)

        position = GeometryUtils.closest_point_on_line_segment(
            (robot.x, robot.y),
            position1,
            position2)

        return self._move_reward(position)

    def _actions_to_v_wheels(
        self,
        actions: np.ndarray
    ):
        left_wheel_speed = actions[1] * self.max_v
        right_wheel_speed = actions[0] * self.max_v

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

        left_wheel_speed /= self.field_params.rbt_wheel_radius
        right_wheel_speed /= self.field_params.rbt_wheel_radius

        return left_wheel_speed, right_wheel_speed
