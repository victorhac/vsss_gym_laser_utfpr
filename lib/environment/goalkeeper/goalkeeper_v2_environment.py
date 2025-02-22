import numpy as np
from gymnasium.spaces import Box
from rsoccer_gym.Entities import Robot
from lib.domain.curriculum_task import CurriculumTask
from lib.environment.base_curriculum_environment import BaseCurriculumEnvironment
from lib.utils.geometry_utils import GeometryUtils
from lib.utils.rsoccer.rsoccer_utils import RSoccerUtils

class GoalkeeperV2Environment(BaseCurriculumEnvironment):
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
            shape=(9,),
            dtype=np.float32)

        self.is_yellow_team = False
        self.threshold_ball = .07
        self.touched_ball = False

    def reset(
        self,
        *,
        seed=None,
        options=None
    ):
        self.touched_ball = False
        return super().reset(seed=seed, options=options)

    def _is_done(self):
        if self._any_team_scored_goal():
            return True
        elif self._is_ball_cleared_from_goal_area():
            return True
        elif self._has_episode_time_exceeded():
            return True
        return False
    
    def _is_ball_cleared_from_goal_area(self):
        if self.touched_ball and not self._is_ball_inside_goal_area():
            return True
        return False

    def _frame_to_observations(self):
        observation = []

        current_robot = self._get_robot_by_id(
            self.robot_id,
            self.is_yellow_team
        )
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

        extend_observation_by_robot(frame.robots_blue[0])

        return np.array(observation, dtype=np.float32)

    def _move_towards_ball_reward(self):
        ball = self._get_ball()
        return self._move_reward((ball.x, ball.y))

    def _calculate_reward_and_done(self):
        is_done = self._is_done()
        reward = self._get_reward()

        if is_done:
            if self._any_team_scored_goal() and self._has_received_goal():
                reward = -10
                self.last_game_score = -1
            elif self._is_ball_cleared_from_goal_area():
                reward = 10
                self.last_game_score = 1
            else:
                self.last_game_score = None

        if not self._is_ball_inside_goal_area():
            self.touched_ball = False
        else:
            self._try_set_touched_ball()

        return reward, is_done
    
    def _get_ball_gradient_towards_center_line_reward(self):
        ball = self._get_ball()
        own_goal_position = self.get_inside_own_goal_position(self.is_yellow_team)
        defensive_line_position = (0.65, ball.y)

        return self._ball_gradient_reward_by_positions(
            self.previous_ball_potential,
            defensive_line_position,
            own_goal_position)

    def _get_reward(self):
        robot = self._get_agent()

        robot_position = (robot.x, robot.y)

        is_inside_own_goal_area = self._is_inside_own_goal_area(
            robot_position,
            self.is_yellow_team)

        is_inside_playable_field = self._is_inside_playable_field(
            robot_position)

        if not is_inside_own_goal_area or not is_inside_playable_field:
            w_move = 0.2
            w_energy = 2e-4

            x, y = -0.675, self._get_y_target()
            return -2 +\
                w_move * self._move_reward((x, y)) +\
                w_energy * self._energy_penalty()

        if self._is_ball_inside_goal_area():
            w_move = 0.2
            w_ball_gradient = 0.8
            w_energy = 2e-4

            ball = self._get_ball()

            ball_gradient_reward, self.previous_ball_potential = \
                self._get_ball_gradient_towards_center_line_reward()

            move_reward = self._move_reward((ball.x, ball.y))
            energy_penalty = self._energy_penalty()

            reward = w_move * move_reward + \
                w_ball_gradient * ball_gradient_reward + \
                w_energy * energy_penalty
        else:
            self.previous_ball_potential = None

            w_energy = 4e-4
            w_alignment = 1

            reward = w_alignment * self._get_alignment_reward() + \
                w_energy * self._energy_penalty()

        return reward
    
    def _try_set_touched_ball(self):
        if self._is_ball_inside_goal_area():
            robot = self._get_agent()
            ball = self._get_ball()

            if GeometryUtils.is_close(
                (robot.x, robot.y),
                (ball.x, ball.y),
                self.threshold_ball
            ):
                self.touched_ball = True

    def _is_ball_inside_goal_area(self):
        ball = self._get_ball()
        return self._is_inside_own_goal_area(
            (ball.x, ball.y),
            self.is_yellow_team)
    
    def _get_y_target(self):
        ball = self._get_ball()
        robot_radius = self.get_robot_radius() + 0.03
        goal_line_x = -self.get_field_length() / 2
        goal_y_max = self.get_goal_width() / 2
        goal_y_min = -goal_y_max

        y_target = 0

        def get_y_target():
            if ball.y > goal_y_max:
                return goal_y_max - robot_radius
            elif ball.y < goal_y_min:
                return goal_y_min + robot_radius
            else:
                return ball.y

        if ball.v_x >= 0:
            y_target = get_y_target()
        else:
            t = (goal_line_x - ball.x) / ball.v_x
            intersection_y = ball.y + t * ball.v_y

            if not (goal_y_min <= intersection_y <= goal_y_max):
                y_target = get_y_target()
            else:
                y_target = intersection_y

        return y_target

    def _get_alignment_reward(self):
        robot = self._get_agent()

        robot_radius = self.get_robot_radius()

        field_width = self.get_field_width()
        goal_y_max = self.get_goal_width() / 2
        goal_y_min = -goal_y_max

        y_target = self._get_y_target()

        max_distance = abs(field_width / 2 - goal_y_min + robot_radius)
        distance_to_target = abs(robot.y - y_target)

        return (1 - distance_to_target / max_distance) * 2 - 1
    
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

        left_wheel_speed /= self.field.rbt_wheel_radius
        right_wheel_speed /= self.field.rbt_wheel_radius

        return left_wheel_speed, right_wheel_speed
