from rsoccer_gym.Entities import Robot as RSoccerRobot
from lib.domain.robot import Robot
from lib.domain.field import Field
from lib.environment.base_environment import BaseEnvironment
from lib.utils.geometry_utils import GeometryUtils
from lib.utils.rsoccer_utils import RSoccerUtils
import numpy as np

class AttackerEnvironmentUtils:
    @staticmethod
    def get_observation(
        base_environment: BaseEnvironment,
        robot_id: int,
        is_yellow: bool,
        is_left_team: bool
    ):
        observation = []

        def get_norm_theta(robot: RSoccerRobot):
            return RSoccerUtils.get_norm_theta_by_rsoccer_robot(robot, is_left_team)
        
        def get_x_and_y(x: float, y: float):
            return RSoccerUtils.get_x_and_y(x, y, is_left_team)

        def get_normalized_distance(distance: float):
            return distance / base_environment._get_max_distance()
        
        current_robot = base_environment._get_robot_by_id(robot_id, is_yellow)
        current_robot_position = get_x_and_y(current_robot.x, current_robot.y)
        ball = base_environment._get_ball()

        def extend_observation_by_ball():
            ball_position = get_x_and_y(ball.x, ball.y)
            velocity = get_x_and_y(ball.v_x, ball.v_y)

            distance = GeometryUtils.distance(current_robot_position, ball_position)
            angle = GeometryUtils.angle_between_points(current_robot_position, ball_position)

            observation.extend([
                get_normalized_distance(distance),
                angle / np.pi,
                base_environment.norm_v(velocity[0]),
                base_environment.norm_v(velocity[1])
            ])

        def extend_observation_by_current_robot():
            position = get_x_and_y(current_robot.x, current_robot.y)
            velocity = get_x_and_y(current_robot.v_x, current_robot.v_y)

            observation.extend([
                base_environment.norm_x(position[0]),
                base_environment.norm_y(position[1]),
                get_norm_theta(current_robot),
                base_environment.norm_v(velocity[0]),
                base_environment.norm_v(velocity[1])
            ])

        def extend_observation_by_robot(robot: RSoccerRobot):
            if base_environment._is_inside_field((robot.x, robot.y)):
                theta = get_norm_theta(robot)

                robot_position = get_x_and_y(robot.x, robot.y)
                velocity = get_x_and_y(robot.v_x, robot.v_y)

                distance = GeometryUtils.distance(current_robot_position, robot_position)
                angle = GeometryUtils.angle_between_points(current_robot_position, robot_position)

                observation.extend([
                    get_normalized_distance(distance),
                    angle / np.pi,
                    theta,
                    base_environment.norm_v(velocity[0]),
                    base_environment.norm_v(velocity[1])
                ])
            else:
                observation.extend([0, 0, 0, 0, 0])

        extend_observation_by_ball()
        extend_observation_by_current_robot()

        team, foe_team = RSoccerUtils.get_team_and_foe_team(base_environment, is_yellow)

        for i in range(3):
            if i != robot_id:
                extend_observation_by_robot(team[i])

        for i in range(3):
            extend_observation_by_robot(foe_team[i])

        return np.array(observation, dtype=np.float32)
    
    @staticmethod
    def get_observation_by_field(
        field: Field,
        robot_id: int,
        is_left_team: bool
    ):
        observation = []

        def get_norm_theta(robot: Robot):
            return RSoccerUtils.get_norm_theta_by_robot(robot, is_left_team)
        
        def get_x_and_y(x: float, y: float):
            return RSoccerUtils.get_x_and_y(x, y, is_left_team)

        def get_normalized_distance(distance: float):
            return RSoccerUtils.get_normalized_distance(distance)

        def norm_v(v: float):
            return RSoccerUtils.norm_v(v)

        def norm_x(x: float):
            return RSoccerUtils.norm_x(x)
        
        def norm_y(y: float):
            return RSoccerUtils.norm_y(y)
        
        def is_inside_field(x: float, y: float):
            return RSoccerUtils.is_inside_field(x, y)
        
        current_robot = field.robots[robot_id]
        current_robot_position = get_x_and_y(current_robot.position.x, current_robot.position.y)
        ball = field.ball

        def extend_observation_by_ball():
            ball_position = get_x_and_y(ball.position.x, ball.position.y)
            velocity = get_x_and_y(ball.velocity.x, ball.velocity.y)

            distance = GeometryUtils.distance(current_robot_position, ball_position)
            angle = GeometryUtils.angle_between_points(current_robot_position, ball_position)

            observation.extend([
                get_normalized_distance(distance),
                angle / np.pi,
                norm_v(velocity[0]),
                norm_v(velocity[1])
            ])

        def extend_observation_by_current_robot():
            position = get_x_and_y(current_robot.position.x, current_robot.position.y)
            velocity = get_x_and_y(current_robot.velocity.x, current_robot.velocity.y)

            observation.extend([
                norm_x(position[0]),
                norm_y(position[1]),
                get_norm_theta(current_robot),
                norm_v(velocity[0]),
                norm_v(velocity[1])
            ])

        def extend_observation_by_robot(robot: RSoccerRobot):
            if is_inside_field(robot.x, robot.y):
                theta = get_norm_theta(robot)

                robot_position = get_x_and_y(robot.x, robot.y)
                velocity = get_x_and_y(robot.v_x, robot.v_y)

                distance = GeometryUtils.distance(current_robot_position, robot_position)
                angle = GeometryUtils.angle_between_points(current_robot_position, robot_position)

                observation.extend([
                    get_normalized_distance(distance),
                    angle / np.pi,
                    theta,
                    norm_v(velocity[0]),
                    norm_v(velocity[1])
                ])
            else:
                observation.extend([0, 0, 0, 0, 0])

        extend_observation_by_ball()
        extend_observation_by_current_robot()

        for i in range(3):
            if i != robot_id:
                extend_observation_by_robot(field.robots[i])

        for i in range(3):
            extend_observation_by_robot(field.foes[i])

        return np.array(observation, dtype=np.float32)