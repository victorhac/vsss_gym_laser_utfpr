import numpy as np
from gymnasium.spaces import MultiDiscrete, Box
from rsoccer_gym.Entities import Robot
from lib.domain.curriculum_task import CurriculumTask
from lib.domain.enums.role_enum import RoleEnum
from lib.domain.robot_curriculum_behavior import RobotCurriculumBehavior
from lib.domain.enums.robot_curriculum_behavior_enum import RobotCurriculumBehaviorEnum
from lib.environment.base_curriculum_environment import BaseCurriculumEnvironment
from lib.positioning.default_supporter_positioning import get_supporter_position
from lib.utils.field_utils import FieldUtils
from lib.utils.model_utils import ModelUtils
from lib.utils.motion_utils import MotionUtils
from lib.utils.roles.attacker_utils import AttackerUtils
from lib.utils.geometry_utils import GeometryUtils
from lib.utils.roles.defender_utils import DefenderUtils
from lib.utils.roles.goalkeeper_utils import GoalkeeperUtils
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
            shape=(35,),
            dtype=np.float32)

        self.is_yellow_team = False
        self.robot_blocking_time_threshold = 2

        self.distance_to_unblock = 0.05
        self.time_to_ball_deadlock = 10
        self.first_ball_blocked_time = None
        self.last_ball_position = None

        self.blocked_robots = {
            0: None,
            1: None,
            2: None
        }

        self.attacker_model = ModelUtils.get_attacker_model()
        self.defender_model = ModelUtils.get_defender_model()
        self.goalkeeper_model = ModelUtils.get_goalkeeper_model()

    def reset(
        self,
        *,
        seed=None,
        options=None
    ):
        self.blocked_robots = {
            0: None,
            1: None,
            2: None
        }
        self.first_ball_blocked_time = None
        self.first_ball_blocked_position = None
        return super().reset(seed=seed, options=options)

    def _is_done(self):
        if self._any_team_scored_goal():
            return True
        elif self._has_episode_time_exceeded():
            return True
        elif self._are_two_robots_and_ball_inside_own_goal_area():
            return True
        elif self._is_ball_deadlocked():
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
            action = self.attacker_model.predict(observation)[0]
            left_speed, right_speed = self._actions_to_v_wheels(action)
        elif role_enum == RoleEnum.DEFENDER:
            observation = self._frame_to_defender_observation(robot_id, is_yellow)
            action = self.defender_model.predict(observation)[0]
            left_speed, right_speed = self._actions_to_v_wheels(action)
        elif role_enum == RoleEnum.GOALKEEPER:
            observation = self._frame_to_goalkeeper_observation(robot_id, is_yellow)
            action = self.goalkeeper_model.predict(observation)[0]
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

        return self._create_robot_command(
            behavior.robot_id,
            behavior.is_yellow,
            0,
            0)
    
    def _get_observation_by_behavior(
        self,
        behavior: RobotCurriculumBehavior
    ):
        def frame_to_observation(frame_to_observation_function):
            return frame_to_observation_function(
                behavior.robot_id,
                behavior.is_yellow)
    
        if behavior.role_enum == RoleEnum.DEFENDER:
            return frame_to_observation(self._frame_to_defender_observation)
        elif behavior.role_enum == RoleEnum.GOALKEEPER:
            return frame_to_observation(self._frame_to_goalkeeper_observation)
        
        return frame_to_observation(self._frame_to_attacker_observation)

    def _get_from_model_actions(self, behavior: RobotCurriculumBehavior):
        model = self._update_model(
            behavior.robot_id,
            behavior.is_yellow,
            behavior.model_path)

        if model is None:
            return (0, 0)

        return model.predict(
            self._get_observation_by_behavior(behavior)
        )[0]

    def _move_towards_ball_reward(self, robot_id: int):
        ball = self._get_ball()
        return self._move_reward((ball.x, ball.y), robot_id)

    def _calculate_reward_and_done(self):
        reward = self._get_reward()

        self._try_set_blocked_robots()
        self._try_set_first_ball_blocked_time()

        is_done = self._is_done()

        if is_done:
            if self._any_team_scored_goal():
                reward = 10 if self._has_scored_goal() else -10
                reward *= 1 - self._get_time_factor()
                self.last_game_score = 1
            elif self._is_ball_deadlocked():
                reward = -2.5
                self.last_game_score = -0.25
            elif self._are_two_robots_and_ball_inside_own_goal_area():
                reward = -5
                self.last_game_score = -0.5
            elif self._has_episode_time_exceeded():
                self.last_game_score = 0

        return reward, is_done
    
    def _get_commands(self, action):
        commands = []

        for i in range(self.n_robots_blue):
            behavior = self.task.get_blue_behaviors_by_robot_id(i)

            if behavior is None:
                commands.append(self._create_robot_command(i, False, 0, 0))
            else:
                commands.append(self._create_robot_command_by_behavior(
                    behavior,
                    RoleEnum(action[i])
                ))

        for i in range(self.n_robots_yellow):
            behavior = self.task.get_yellow_behaviors_by_robot_id(i)

            if behavior is None:
                commands.append(self._create_robot_command(i, True, 0, 0))
            else:
                commands.append(self._create_robot_command_by_behavior(behavior))

        return commands

    def _get_reward(self):
        w_move = 0.2
        w_ball_gradient = 0.8

        ball = self._get_ball()

        if ball.v_x < 0:
            w_defensive = 0.4
            w_blocked_robot = 0.4
            w_crowded_robot = 0.2

            defensive_penalty = self._get_defensive_penalty()

            penalty = w_defensive * defensive_penalty +\
                w_blocked_robot * self._get_blocked_robot_penalty() +\
                w_crowded_robot * self._get_crowded_robot_penalty()
        else:
            w_blocked_robot = 0.6
            w_crowded_robot = 0.4

            penalty = w_blocked_robot * self._get_blocked_robot_penalty() +\
                w_crowded_robot * self._get_crowded_robot_penalty()

        return w_move * self._get_move_towards_ball_reward() +\
            w_ball_gradient * self._get_ball_gradient_reward() +\
            penalty

    def _get_move_towards_ball_reward(self):
        ball = self._get_ball()
        robot = self._get_team_robot_closest_to_position((ball.x, ball.y))
        return self._move_towards_ball_reward(robot.id)
    
    def _get_ball_gradient_reward(self):
        previous_ball_potential = self.previous_ball_potential

        reward, self.previous_ball_potential =\
            self._ball_gradient_reward_by_positions(
                previous_ball_potential,
                self.get_inside_own_goal_position(True),
                self.get_inside_own_goal_position(False))
        
        if previous_ball_potential is not None and abs(reward) < 0.01:
            reward = -1
        
        return reward
    
    def _get_defensive_penalty(self):
        ball = self._get_ball()
        robots = self._get_active_team_robots()
        own_goal_position = self._get_own_goal_position()

        r_def = -1

        for robot in robots:
            current_r_def = TrainingUtils.r_def(
                RSoccerUtils.to_robot(robot),
                RSoccerUtils.to_ball(ball),
                own_goal_position)
            
            if current_r_def > r_def:
                r_def = current_r_def

        return r_def

    def _get_blocked_robot_penalty(self):
        for robot_id in self.blocked_robots.keys():
            blocked_time = self.blocked_robots[robot_id]
            if blocked_time is not None and\
                    self._get_episode_elapsed_time() - blocked_time > self.robot_blocking_time_threshold:
                return -1
        return 0

    def _get_crowded_robot_penalty(self):
        crowding_distance = 0.1

        robots = self._get_robots_outside_own_goal_area()

        if len(robots) == 1:
            return 0

        for item in robots:
            for item2 in robots:
                if item.id != item2.id and\
                        GeometryUtils.distance(
                            (item.x, item.y),
                            (item2.x, item2.y)) < crowding_distance:
                    return -1

        return 0
    
    def _get_robots_outside_own_goal_area(self):
        return list(
            filter(
                lambda item: not self._is_inside_own_goal_area(
                    (item.x, item.y),
                    False),
                self._get_active_team_robots()
            ))
    
    def _get_active_robot_by_id(self, robot_id: int):
        robots = self._get_active_team_robots()
        return next(
            filter(
                lambda item: item.id == robot_id,
                robots
            ))

    def _try_set_blocked_robots(self):
        robots = self._get_robots_outside_own_goal_area()
        close_to_wall_tolerance = 0.1
        current_blocked_robots = []

        for robot in robots:
            if self._is_close_to_wall(
                (robot.x, robot.y),
                close_to_wall_tolerance
            ):
                current_blocked_robots.append(robot.id)

        for robot_id in self.blocked_robots.keys():
            if robot_id in current_blocked_robots:
                if self.blocked_robots[robot_id] is None:
                    self.blocked_robots[robot_id] = self._get_episode_elapsed_time()
            else:
                self.blocked_robots[robot_id] = None

    def _try_set_first_ball_blocked_time(self):
        ball = self._get_ball()
        if self.first_ball_blocked_time is None:
            self.first_ball_blocked_time = self._get_episode_elapsed_time()
            self.first_ball_blocked_position = (ball.x, ball.y)
        else:
            if GeometryUtils.distance(
                (ball.x, ball.y),
                self.first_ball_blocked_position
            ) > self.distance_to_unblock:
                self.first_ball_blocked_time = None
                self.first_ball_blocked_position = None

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
            key=lambda robot: GeometryUtils.distance(
                (robot.x, robot.y),
                position
            ))
    
    def _is_ball_deadlocked(self):
        if self.first_ball_blocked_time is None:
            return False

        return self._get_episode_elapsed_time() - self.first_ball_blocked_time\
            > self.time_to_ball_deadlock
    
    def _are_two_robots_and_ball_inside_own_goal_area(self):
        ball = self._get_ball()

        def is_inside_own_goal_area(x: float, y: float):
            return self._is_inside_own_goal_area((x, y), False)

        if not is_inside_own_goal_area(ball.x, ball.y):
            return False

        robots = self._get_robots_outside_own_goal_area()
        count = 0

        if len(robots) < 2:
            return False

        for robot in robots:
            if self._is_inside_own_goal_area((robot.x, robot.y), False):
                count += 1

        return count >= 2