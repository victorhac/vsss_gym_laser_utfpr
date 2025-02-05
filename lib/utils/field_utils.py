import random
import math

from lib.domain.ball import Ball
from lib.domain.field import Field
from lib.domain.robot import Robot
from lib.domain.univector_field_navigation.obstacle import Obstacle
from lib.utils.geometry_utils import GeometryUtils

class FieldUtils:
    @staticmethod
    def is_left_team(is_yellow_yeam: bool, is_yellow_left_team: bool):
        return is_yellow_left_team == is_yellow_yeam

    @staticmethod
    def is_inside_field(
        x: float,
        y: float,
        field_length: float,
        field_width: float,
        goal_width: float,
        goal_depth: float
    ):
        if abs(y) < goal_width / 2:
            return abs(x) < (field_length / 2 + goal_depth)

        return abs(x) < field_length / 2 and abs(y) < field_width / 2
    
    @staticmethod
    def is_inside_playable_field(
        x: float,
        y: float,
        field_length: float,
        field_width: float
    ):
        return abs(x) < field_length / 2 and abs(y) < field_width / 2

    @staticmethod
    def get_opponent_goal_position(
        field_length: float,
        is_left_team: bool
    ):
        if is_left_team:
            return (field_length / 2, 0)

        return (-field_length / 2, 0)

    @staticmethod
    def get_own_goal_position(
        field_length: float,
        is_left_team: bool
    ):
        if is_left_team:
            return (-field_length / 2, 0)
        else:
            return (field_length / 2, 0)

    @staticmethod
    def get_inside_own_goal_position(
        field_length: float,
        goal_depth: float,
        is_left_team: bool
    ):
        x, y = FieldUtils.get_own_goal_position(
            field_length,
            is_left_team)

        if x > 0:
            return x + goal_depth, y
        else:
            return x - goal_depth, y

    @staticmethod
    def is_inside_own_goal_area(
        position: 'tuple[float, float]',
        field_length: float,
        goal_area_length: float,
        goal_area_width: float,
        is_left_team: bool
    ):
        x, y = position

        if is_left_team:
            return x < -field_length / 2 + goal_area_length and abs(y) < goal_area_width / 2

        return x > field_length / 2 - goal_area_length and abs(y) < goal_area_width / 2

    @staticmethod
    def is_inside_opponent_area(
        position: 'tuple[float, float]',
        is_left_team: bool
    ):
        x, _ = position

        if is_left_team:
            return x > 0

        return x < 0

    @staticmethod
    def is_touching(
        position1: 'tuple[float, float]',
        radius1: float,
        position2: 'tuple[float, float]',
        radius2: float,
        threshold: float
    ):
        return GeometryUtils.circunferences_intersect(
            position1,
            radius1 + threshold,
            position2,
            radius2 + threshold
        )

    @staticmethod
    def get_random_position_inside_field(
        field_length: float,
        field_width: float,
        margin = 0.1
    ):
        max_x = field_length / 2
        max_y = field_width / 2

        return \
            random.uniform(-max_x + margin, max_x - margin), \
            random.uniform(-max_y + margin, max_y - margin)

    @staticmethod
    def get_random_position_inside_own_area(
        field_length: float,
        field_width: float,
        is_left_team: bool,
        margin = 0.1
    ):
        max_x = field_length / 2
        max_y = field_width / 2

        y = random.uniform(-max_y + margin, max_y - margin)

        if is_left_team:
            return random.uniform(-max_x + margin, 0), y
        else:
            return random.uniform(0, max_x - margin), y

    @staticmethod
    def get_random_position_inside_own_area_except_goal_area(
        field_length: float,
        field_width: float,
        goal_area_length: float,
        goal_area_width: float,
        is_left_team: bool,
        margin = 0.1
    ):
        def get_random_position_inside_own_area():
            return FieldUtils.get_random_position_inside_own_area(
                field_length,
                field_width,
                is_left_team,
                margin
            )

        position = get_random_position_inside_own_area()

        while FieldUtils.is_inside_own_goal_area(
            position,
            field_length,
            goal_area_length,
            goal_area_width,
            is_left_team
        ):
            position = get_random_position_inside_own_area()

        return position

    @staticmethod
    def get_random_position_inside_opponent_area_except_goal_area(
        field_length: float,
        field_width: float,
        goal_area_length: float,
        goal_area_width: float,
        is_left_team: bool,
        margin = 0.1
    ):
        return FieldUtils.get_random_position_inside_own_area_except_goal_area(
            field_length,
            field_width,
            goal_area_length,
            goal_area_width,
            not is_left_team,
            margin
        )

    @staticmethod
    def get_random_position_inside_opponent_area(
        field_length: float,
        field_width: float,
        is_left_team: bool,
    ):
        return FieldUtils.get_random_position_inside_own_area(
            field_length,
            field_width,
            not is_left_team)

    @staticmethod
    def get_random_position_inside_own_goal_area(
        field_length: float,
        goal_area_length: float,
        goal_area_width: float,
        is_left_team: bool
    ):
        max_x = field_length / 2
        max_y = goal_area_width / 2

        x = max_x - random.uniform(0, goal_area_length)
        y = random.uniform(-max_y, max_y)

        if is_left_team:
            return -x, y
        else:
            return x, y

    @staticmethod  
    def get_random_position_at_distance(
        field_length,
        field_width,
        position,
        distance,
        margin = 0.1
    ):
        x, y = position

        (x_min, x_max) = (-field_length / 2 + margin, field_length / 2 - margin)
        (y_min, y_max) = (-field_width / 2 + margin, field_width / 2 - margin)

        while True:
            angle = random.uniform(0, 2 * math.pi)

            new_x = x + distance * math.cos(angle)
            new_y = y + distance * math.sin(angle)

            if x_min <= new_x <= x_max and y_min <= new_y <= y_max:
                return new_x, new_y

    @staticmethod
    def get_position_close_to_wall_relative_to_own_goal(
        field_length: float,
        field_width: float,
        goal_width: float,
        distance: float,
        distance_to_wall: float,
        is_left_team: bool,
        upper: bool
    ):
        half_field_width = field_width / 2
        half_goal_width = goal_width / 2
        vertical_wall_size = (field_width - goal_width) / 2
        horizontal_wall_size = field_length

        max_distance = horizontal_wall_size + 2 * vertical_wall_size
        corrected_distance = distance % max_distance

        goal_position = FieldUtils.get_own_goal_position(
            field_length,
            True
        )

        corner_1_first_distance = vertical_wall_size - distance_to_wall
        corner_1_second_distance = vertical_wall_size + distance_to_wall
        corner_2_first_distance = vertical_wall_size + horizontal_wall_size - distance_to_wall
        corner_2_second_distance = vertical_wall_size + horizontal_wall_size + distance_to_wall

        if 0 <= corrected_distance < corner_1_first_distance:
            x = goal_position[0] + distance_to_wall
            y = distance + half_goal_width
        elif corner_1_first_distance <= corrected_distance <= corner_1_second_distance:
            x = goal_position[0] + distance_to_wall
            y = half_field_width - distance_to_wall
        elif corrected_distance < corner_2_first_distance:
            x = goal_position[0] + (corrected_distance - vertical_wall_size)
            y = half_field_width - distance_to_wall
        elif corner_2_first_distance <= corrected_distance <= corner_2_second_distance:
            x = -(goal_position[0] + distance_to_wall)
            y = half_field_width - distance_to_wall
        else:
            x = -(goal_position[0] + distance_to_wall)
            y = half_goal_width + (max_distance - corrected_distance)

        if not upper:
            y = -y

        if is_left_team:
            return x, y
        
        return -x, -y
    
    @staticmethod
    def get_random_position_at_distance_to_vertical_line(
        distance: float,
        x_line: float,
        y_range: 'tuple[float, float]',
        left_to_line: bool,
        is_left_team: bool
    ):
        side_distance = -distance if left_to_line else distance
        magnitude = y_range[1] - y_range[0]
        t = random.uniform(0, 1)

        x = x_line + side_distance
        y = y_range[0] + t * magnitude

        if is_left_team:
            return x, y

        return -x, -y

    @staticmethod
    def is_inside_goal_area(
        position: 'tuple[float, float]',
        field_length: float,
        goal_area_length: float,
        goal_area_width: float
    ):
        x, y = position

        return (abs(x) > field_length / 2 - goal_area_length) and (abs(y) < goal_area_width / 2)
    
    @staticmethod
    def to_obstacles(
        obstacles: 'list[(Robot | Ball)]'
    ):
        return [
            Obstacle(
                item.get_position_tuple(),
                item.get_velocity_tuple()
            )
            for item in obstacles
        ]
    
    @staticmethod
    def to_obstacles_except_current_robot_and_ball(
        field: Field,
        current_robot_id: int
    ):
        team_robots = []

        for robot in field.get_active_robots():
            if robot.id != current_robot_id:
                team_robots.append(robot)

        obstacles = field.get_active_foes()
        obstacles.extend(team_robots)

        return FieldUtils.to_obstacles(obstacles)
    
    @staticmethod
    def to_obstacles_except_current_robot(
        field: Field,
        current_robot_id: int
    ):
        team_robots = []

        for robot in field.get_active_robots():
            if robot.id != current_robot_id:
                team_robots.append(robot)

        obstacles = field.get_active_foes()
        obstacles.extend(team_robots)
        obstacles.append(field.ball)

        return FieldUtils.to_obstacles(obstacles)
    
    def is_close_to_wall(
        position: 'tuple[float, float]',
        field_length: float,
        field_width: float,
        tolerance: float
    ):
        #TODO: change to consider the goal area
        x, y = position

        return abs(x) > field_length / 2 - tolerance or abs(y) > field_width / 2 - tolerance
    
    @staticmethod
    def get_quadrant(
        position: 'tuple[float, float]'
    ):
        x, y = position

        if x > 0:
            if y > 0:
                return 1
            return 4

        if y > 0:
            return 2
        return 3