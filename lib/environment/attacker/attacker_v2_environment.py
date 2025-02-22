import numpy as np
from gymnasium.spaces import Box
from rsoccer_gym.Entities import Robot
from lib.domain.curriculum_task import CurriculumTask
from lib.environment.base_curriculum_environment import BaseCurriculumEnvironment
from lib.utils.rsoccer.rsoccer_utils import RSoccerUtils

class AttackerV2Environment(BaseCurriculumEnvironment):
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
            shape=(35,),
            dtype=np.float32)

    def _is_done(self):
        if self._any_team_scored_goal():
            return True
        elif self._has_episode_time_exceeded():
            return True
        return False

    def _frame_to_observations(self):
        observation = [
            self._get_time_factor()
        ]

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

    def _ball_gradient_reward(self):
        reward, self.previous_ball_potential =\
            self._ball_gradient_reward_by_positions(
                self.previous_ball_potential,
                self.get_inside_own_goal_position(is_yellow_team=True),
                self.get_inside_own_goal_position(is_yellow_team=False))
        
        return reward

    def _move_towards_ball_reward(self):
        ball = self._get_ball()
        return self._move_reward(
            (ball.x, ball.y),
            self.robot_id)

    def _calculate_reward_and_done(self):
        reward = self._get_reward()
        is_done = self._is_done()

        if is_done:
            if self._any_team_scored_goal():
                reward = 10 if self._has_scored_goal() else -10
                reward *= 1 - self._get_time_factor()
                self.last_game_score = 1 if self._has_scored_goal() else -1
            else:
                self.last_game_score = 0

        return reward, is_done

    def _get_reward(self):
        w_move = 0.2
        w_ball_grad = 0.8
        w_energy = 2e-4

        ball_gradient_reward = self._ball_gradient_reward()
        move_reward = self._move_towards_ball_reward()
        energy_penalty = self._energy_penalty()

        return w_move * move_reward + \
            w_ball_grad * ball_gradient_reward + \
            w_energy * energy_penalty

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
