import numpy as np
from gymnasium.spaces import MultiDiscrete, Box
from rsoccer_gym.Entities import Robot
from lib.domain.curriculum_task import CurriculumTask
from lib.domain.enums.role_enum import RoleEnum
from lib.domain.robot_curriculum_behavior import RobotCurriculumBehavior
from lib.domain.enums.robot_curriculum_behavior_enum import RobotCurriculumBehaviorEnum
from lib.environment.base_curriculum_environment import BaseCurriculumEnvironment
from lib.utils.roles.attacker_utils import AttackerUtils
from lib.utils.geometry_utils import GeometryUtils
from lib.utils.rsoccer_utils import RSoccerUtils
from lib.utils.training_utils import TrainingUtils

class TeamEnvironment(BaseCurriculumEnvironment):
    def __init__(
        self,
        task: CurriculumTask,
        render_mode="rgb_array"
    ):
        super().__init__(
            task=task,
            render_mode=render_mode,
            robot_id=0)

        self.action_space = MultiDiscrete([4, 4, 4])

        self.observation_space = Box(
            low=-1,
            high=1,
            shape=(34,),
            dtype=np.float32)

        self.is_yellow_team = False

    def _is_done(self):
        if self._any_team_scored_goal():
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

    def _frame_to_opponent_attacker_observations(self, robot_id: int):
        return AttackerUtils.get_observation(
            self,
            robot_id,
            True,
            False)
    
    def _create_from_model_robot_command(self, behavior: RobotCurriculumBehavior):
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
    
    def _create_robot_command_by_behavior(self, behavior: RobotCurriculumBehavior):
        robot_curriculum_behavior_enum = behavior.robot_curriculum_behavior_enum

        if robot_curriculum_behavior_enum == RobotCurriculumBehaviorEnum.BALL_FOLLOWING:
            return self._create_ball_following_robot_command(behavior)
        elif robot_curriculum_behavior_enum == RobotCurriculumBehaviorEnum.GOALKEEPER_BALL_FOLLOWING:
            return self._create_goalkeeper_ball_following_robot_command(behavior)
        elif robot_curriculum_behavior_enum == RobotCurriculumBehaviorEnum.FROM_PREVIOUS_MODEL or\
            robot_curriculum_behavior_enum == RobotCurriculumBehaviorEnum.FROM_FIXED_MODEL:
            return self._create_from_model_robot_command(behavior)

        return self._create_robot_command(
            behavior.robot_id,
            behavior.is_yellow,
            0,
            0)

    def _get_from_model_actions(self, behavior: RobotCurriculumBehavior):
        model = self._update_model(
            behavior.robot_id,
            behavior.is_yellow,
            behavior.model_path)

        if model is None:
            return (0, 0)

        return model.predict(
            self._frame_to_opponent_attacker_observations(behavior.robot_id)
        )[0]

    def _move_towards_ball_reward(self, robot_id: int):
        ball = self._get_ball()
        return self._move_reward((ball.x, ball.y), robot_id)

    def _calculate_reward_and_done(self):
        reward = self._get_reward()
        is_done = self._is_done()

        return reward, is_done

    def _get_reward(self):
        robot = self._get_agent()

        w_move = 0.2
        w_ball_gradient = 0.8
        w_energy = 2e-4
        w_alignment = 1

        return 0

    def _get_active_team_robots(self):
        behaviors = self.task.get_blue_behaviors()
        return [
            self._get_robot_by_id(item.robot_id, False)
            for item in behaviors
        ]
    
    def _get_team_robot_closest_to_position(self, position: tuple):
        robots = self._get_active_team_robots()
        return max(
            robots,
            key=lambda robot: GeometryUtils.distance((robot.x, robot.y), position))
    
    def _get_move_towards_ball_reward(self):
        ball = self._get_ball()
        robot = self._get_team_robot_closest_to_position((ball.x, ball.y))
        return self._move_towards_ball_reward(robot.id)
    
    def _get_ball_gradient_reward(self):
        return self._ball_gradient_reward_by_positions(
            self.get_inside_own_goal_position(True),
            self.get_inside_own_goal_position(False)
        )
    
    def _get_defensive_reward(self):
        ball = self._get_ball()
        robot = self._get_team_robot_closest_to_position((ball.x, ball.y))
        own_goal_position = self.get_inside_own_goal_position(False)

        return TrainingUtils.r_def(
            robot,
            ball,
            own_goal_position
        )

    def _get_distance_to_ball_reward(self):
        ball = self._get_ball()
        robot = self._get_team_robot_closest_to_position((ball.x, ball.y))
        distance = GeometryUtils.distance(
            (robot.x, robot.y),
            (ball.x, ball.y)
        )
        return 1 - distance / self._get_max_distance()

    def _get_blocked_robot_penalty(self):
        pass

    def _get_crownded_robot_penalty(self):
        pass