import numpy as np
from configuration.configuration import Configuration
from lib.domain.field import Field
from lib.domain.robot import Robot
from lib.path_planning.univector_field_navigation import get_univector_field_point_theta
from lib.path_planning.univector_field_navigation_configuration import UnivectorFieldNavigationConfiguration
from lib.utils.field_utils import FieldUtils
from lib.utils.geometry_utils import GeometryUtils
from lib.utils.motion_utils import MotionUtils

field_length = Configuration.field_length
field_width = Configuration.field_width
goal_area_length = Configuration.field_goal_area_length
goal_area_width = Configuration.field_goal_area_width
max_distance = Configuration.rsoccer_training_max_distance

distance_to_wall = Configuration.positioning_default_supporter_distance_to_wall
considered_length = field_length - 2 * distance_to_wall
considered_width = field_width - 2 * distance_to_wall

x_step_count = Configuration.positioning_default_supporter_x_step_count
y_step_count = Configuration.positioning_default_supporter_y_step_count
ball_min_distance = Configuration.positioning_default_supporter_ball_min_distance
robot_min_distance = Configuration.positioning_default_supporter_robot_min_distance
considered_robot_distance = Configuration.positioning_default_supporter_considered_robot_distance
distance_behind_ball = Configuration.positioning_default_supporter_distance_behind_ball

w_distance_to_robot = Configuration.positioning_default_supporter_weights_distance_to_robot
w_distance_to_position = Configuration.positioning_default_supporter_weights_distance_to_position
w_distance_to_ball = Configuration.positioning_default_supporter_weights_distance_to_ball
w_distance_to_goal = Configuration.positioning_default_supporter_weights_distance_to_goal

def _get_distance(
    position1: 'tuple[float, float]',
    position2: 'tuple[float, float]'
):
    return GeometryUtils.distance(
        position1,
        position2)

def _get_attraction_distance_score(
    current_position: 'tuple[float, float]',
    reference_position: 'tuple[float, float]',
    min_distance: float
):
    distance = _get_distance(
        current_position,
        reference_position)

    if distance < min_distance:
        return 0
    
    return 1 - ((distance - min_distance) / (max_distance - min_distance))

def _get_repulsive_distance_score(
    current_position: 'tuple[float, float]',
    reference_position: 'tuple[float, float]',
    min_distance: float
):
    distance = _get_distance(
        current_position,
        reference_position)

    if distance < min_distance:
        return 0
    
    return (distance - min_distance) / (max_distance - min_distance)

def _get_ball_distance_score(
    position: 'tuple[float, float]',
    field: Field
):
    return _get_attraction_distance_score(
        position,
        field.ball.get_position_tuple(),
        ball_min_distance)

def _get_distance_to_robot_score(
    position: 'tuple[float, float]',
    robot_id: int,
    field: Field
):
    distance_scores = []
    ball_position = field.ball.get_position_tuple()
    robots = field.get_active_robots()
    foes = field.get_active_foes()

    def append_score(robot: Robot):
        distance = _get_distance(
            robot.get_position_tuple(),
            ball_position
        )

        if distance > considered_robot_distance:
            return

        distance_score = _get_repulsive_distance_score(
            position,
            robot.get_position_tuple(),
            robot_min_distance)

        distance_scores.append(distance_score)

    for item in robots:
        if item.id == robot_id:
            continue

        append_score(item)

    for item in foes:
        append_score(item)

    return 1 if len(distance_scores) == 0 else np.mean(distance_scores)

def _get_distance_to_position_score(
    position: 'tuple[float, float]',
    robot_id: int,
    field: Field
):
    robot = field.get_robot_by_id(robot_id)
    return _get_attraction_distance_score(
        position,
        robot.get_position_tuple(),
        0)

def _get_distance_to_goal_score(
    position: 'tuple[float, float]',
    field: Field
):
    ball = field.ball
    is_ball_inside_defensive_area = ball.position.x < 0
    
    if is_ball_inside_defensive_area:
        reference_position = (-field_length / 2, 0)
    else:
        if position[0] > (ball.position.x - distance_behind_ball):
            return 0
        else:
            reference_position = (field_length / 2, 0)

    return _get_attraction_distance_score(
        position,
        reference_position,
        0)

def _is_inside_goal_area(
    position: 'tuple[float, float]'
):
    return FieldUtils.is_inside_goal_area(
        position,
        field_length,
        goal_area_length,
        goal_area_width)

def _get_score(
    robot_id: int,
    field: Field,
    position: 'tuple[float, float]'
):
    if _is_inside_goal_area(position):
        return 0

    distance_to_ball_score = _get_ball_distance_score(
        position,
        field)

    distance_to_position_score = _get_distance_to_position_score(
        position,
        robot_id,
        field)

    distance_to_robot_score = _get_distance_to_robot_score(
        position,
        robot_id,
        field)
    
    distance_to_goal_score = _get_distance_to_goal_score(
        position,
        field)

    return w_distance_to_robot * distance_to_robot_score +\
        w_distance_to_position * distance_to_position_score +\
            w_distance_to_ball * distance_to_ball_score +\
            w_distance_to_goal * distance_to_goal_score

def get_supporter_position(robot_id: int, field: Field):
    x_step = considered_length / (x_step_count + 1)
    y_step = considered_width / (y_step_count + 1)
    max_x, max_y = considered_length / 2, considered_width / 2
    min_x, min_y = -max_x, -max_y

    max_score = -1
    best_position = (0, 0)

    for x in np.arange(min_x, max_x, x_step):
        for y in np.arange(min_y, max_y, y_step):
            position = (x, y)
            score = _get_score(
                robot_id,
                field,
                (x, y))

            if score > max_score:
                max_score = score
                best_position = position

    return best_position

univector_field_navigation_configuration = UnivectorFieldNavigationConfiguration(
    0.0537,
    0.0415,
    0.0012,
    0.0948,
    0.0457
)

def get_supporter_speeds(
    robot_id: int,
    field: Field,
    base_speed: float = 30
):
    robot = field.get_robot_by_id(robot_id)
    target_position = get_supporter_position(robot_id, field)

    if GeometryUtils.is_close(
        robot.get_position_tuple(),
        target_position,
        .05
    ):
        return 0, 0
    
    obstacles = FieldUtils.to_obstacles_except_current_robot_and_ball(
        field,
        robot_id
    )

    theta = get_univector_field_point_theta(
        robot.get_position_tuple(),
        robot.get_velocity_tuple(),
        target_position,
        obstacles,
        univector_field_navigation_configuration
    )

    return MotionUtils.go_to_point_by_theta(
        robot,
        theta,
        base_speed)
