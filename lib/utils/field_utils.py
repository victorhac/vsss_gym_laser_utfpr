import random
import math

from lib.utils.geometry_utils import GeometryUtils

class FieldUtils:
    @staticmethod
    def is_left_team(is_yellow_yeam: bool, is_yellow_left_team: bool):
        return is_yellow_left_team == is_yellow_yeam

    @staticmethod
    def is_inside_field(
        x: float,
        y: float,
        field_width: float,
        field_height: float
    ):
        return abs(x) < field_width / 2 and abs(y) < field_height / 2

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
        margin = 0.15
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
        margin = 0.15
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
        margin = 0.15
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
        margin = 0.15
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
        margin = 0.15
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
            