import numpy as np

from gymnasium.spaces import Box
from rsoccer_gym.Entities import Robot

from lib.domain.curriculum_task import CurriculumTask
from lib.domain.robot_curriculum_behavior import RobotCurriculumBehavior
from lib.domain.enums.robot_curriculum_behavior_enum import RobotCurriculumBehaviorEnum
from lib.environment.base_curriculum_environment import BaseCurriculumEnvironment
from lib.utils.environment.attacker_environment_utils import AttackerEnvironmentUtils
from lib.utils.geometry_utils import GeometryUtils
from lib.utils.rsoccer_utils import RSoccerUtils

class GoalkeeperEnvironment(BaseCurriculumEnvironment):
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

        self.is_yellow_team = False

    def _is_done(self):
        if self._has_episode_time_exceeded():
            return True
        return False

    def _frame_to_observations(self):
        observation = []

        current_robot = self._get_robot_by_id(self.robot_id, self.is_yellow_team)
        ball = self._get_ball()

        def extend_observation_by_ball():
            observation.extend([
                self.norm_x(ball.x),
                self.norm_y(-ball.y),
                self.norm_v(ball.v_x),
                self.norm_v(-ball.v_y)
            ])

        def extend_observation_by_robot(robot: Robot):
            theta = -RSoccerUtils.get_corrected_angle(current_robot.theta) / np.pi

            if self._is_inside_field((robot.x, robot.y)): 
                observation.extend([
                    self.norm_x(robot.x),
                    self.norm_y(-robot.y),
                    theta,
                    self.norm_v(robot.v_x),
                    self.norm_v(-robot.v_y)
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
        return AttackerEnvironmentUtils.get_observation(
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

        ball_potential = ((distance_to_desired - distance_to_undesired) / field_length - 1) / 2

        if previous_ball_potential is not None:
            ball_potential_difference = ball_potential - previous_ball_potential
            reward = np.clip(
                ball_potential_difference * 3 / self.time_step,
                -5.0,
                5.0)
        else:
            reward = 0

        return reward, ball_potential

    def _move_towards_ball_reward(self):
        ball = self._get_ball()
        return self._move_reward((ball.x, ball.y))

    def _move_reward(
        self,
        position: 'tuple[float, float]'
    ):
        robot = self._get_agent()
        robot_position = np.array([robot.x, robot.y])

        robot_velocities = np.array([robot.v_x, robot.v_y])
        robot_ball_vector = np.array(position) - robot_position
        robot_ball_vector = robot_ball_vector / np.linalg.norm(robot_ball_vector)

        move_reward = np.dot(robot_ball_vector, robot_velocities)

        return np.clip(move_reward / 0.4, -5.0, 5.0)

    def _calculate_reward_and_done(self):
        reward = self._get_reward()
        is_done = self._is_done()

        if is_done:
            pass

        return reward, is_done

    def _get_reward(self):
        alignment = self.get_alignment()
        print(alignment)
        return 0

    def _is_ball_inside_goal_area(self):
        ball = self._get_ball()
        return self._is_inside_own_goal_area(
            (ball.x, ball.y),
            self.is_yellow_team)
    
    def get_alignment(self):
        ball = self._get_ball()
        robot = self._get_agent()
        goal_line_x = -self.get_field_length() / 2
        goal_y_max = self.get_goal_width() / 2
        goal_y_min = -goal_y_max

        if ball.v_x >= 0:
            return None

        t = (goal_line_x - ball.x) / ball.v_x
        intersection_y = ball.y + t * ball.v_y

        if not (goal_y_min <= intersection_y <= goal_y_max):
            return None
        
        return np.abs(robot.y - intersection_y)
