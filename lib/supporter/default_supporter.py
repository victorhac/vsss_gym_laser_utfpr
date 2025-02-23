import numpy as np
from configuration.configuration import Configuration
from lib.domain.field import Field
from lib.domain.robot import Robot
from lib.path_planning.univector_field_navigation import get_univector_field_point_theta
from lib.domain.univector_field_navigation.univector_field_navigation_configuration import UnivectorFieldNavigationConfiguration
from lib.utils.field_utils import FieldUtils
from lib.utils.geometry_utils import GeometryUtils
from lib.utils.motion_utils import MotionUtils

FIELD_LENGTH = Configuration.field_length
FIELD_WIDTH = Configuration.field_width
GOAL_AREA_LENGTH = Configuration.field_goal_area_length
GOAL_AREA_WIDTH = Configuration.field_goal_area_width
MAX_DISTANCE = Configuration.rsoccer_training_max_distance

DISTANCE_TO_WALL = Configuration.supporter_distance_to_wall
CONSIDERED_LENGTH = FIELD_LENGTH - 2 * DISTANCE_TO_WALL
CONSIDERED_WIDTH = FIELD_WIDTH - 2 * DISTANCE_TO_WALL

X_STEP_COUNT = Configuration.supporter_x_step_count
Y_STEP_COUNT = Configuration.supporter_y_step_count
BALL_MIN_DISTANCE = Configuration.supporter_ball_min_distance
ROBOT_MIN_DISTANCE = Configuration.supporter_robot_min_distance
CONSIDERED_ROBOT_DISTANCE = Configuration.supporter_considered_robot_distance
DISTANCE_BEHIND_BALL = Configuration.supporter_distance_behind_ball

W_DISTANCE_TO_ROBOT = Configuration.supporter_weights_distance_to_robot
W_DISTANCE_TO_POSITION = Configuration.supporter_weights_distance_to_position
W_DISTANCE_TO_BALL = Configuration.supporter_weights_distance_to_ball
W_DISTANCE_TO_GOAL = Configuration.supporter_weights_distance_to_goal

univector_field_navigation_configuration = UnivectorFieldNavigationConfiguration(
    Configuration.supporter_univector_field_navigation_de,
    Configuration.supporter_univector_field_navigation_kr,
    Configuration.supporter_univector_field_navigation_k0,
    Configuration.supporter_univector_field_navigation_dmin,
    Configuration.supporter_univector_field_navigation_gaussian_delta
)

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
    
    return 1 - ((distance - min_distance) / (MAX_DISTANCE - min_distance))

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
    
    return (distance - min_distance) / (MAX_DISTANCE - min_distance)

def _get_ball_distance_score(
    position: 'tuple[float, float]',
    field: Field
):
    return _get_attraction_distance_score(
        position,
        field.ball.get_position_tuple(),
        BALL_MIN_DISTANCE)

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

        if distance > CONSIDERED_ROBOT_DISTANCE:
            return

        distance_score = _get_repulsive_distance_score(
            position,
            robot.get_position_tuple(),
            ROBOT_MIN_DISTANCE)

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
        reference_position = (-FIELD_LENGTH / 2, 0)
    else:
        if position[0] > (ball.position.x - DISTANCE_BEHIND_BALL):
            return 0
        else:
            reference_position = (FIELD_LENGTH / 2, 0)

    return _get_attraction_distance_score(
        position,
        reference_position,
        0)

def _is_inside_goal_area(
    position: 'tuple[float, float]'
):
    return FieldUtils.is_inside_goal_area(
        position,
        FIELD_LENGTH,
        GOAL_AREA_LENGTH,
        GOAL_AREA_WIDTH)

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

    return W_DISTANCE_TO_ROBOT * distance_to_robot_score +\
        W_DISTANCE_TO_POSITION * distance_to_position_score +\
            W_DISTANCE_TO_BALL * distance_to_ball_score +\
            W_DISTANCE_TO_GOAL * distance_to_goal_score

def get_supporter_position(robot_id: int, field: Field):
    x_step = CONSIDERED_LENGTH / (X_STEP_COUNT + 1)
    y_step = CONSIDERED_WIDTH / (Y_STEP_COUNT + 1)
    max_x, max_y = CONSIDERED_LENGTH / 2, CONSIDERED_WIDTH / 2
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

def get_supporter_speeds(
    robot_id: int,
    field: Field,
    base_speed: float = Configuration.team_max_motor_speed
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
