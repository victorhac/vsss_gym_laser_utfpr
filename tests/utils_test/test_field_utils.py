import unittest

from configuration.configuration import Configuration
from lib.utils.field_utils import FieldUtils

class TestFieldUtils(unittest.TestCase):
    def test_get_position_close_to_wall_relative_to_own_goal(self):
        distance = 2.03
        distance_to_wall = .07
        is_left_team = True
        upper = True

        field_length = Configuration.get_field_length()
        field_width = Configuration.get_field_width()
        field_goal_width = Configuration.get_field_goal_width()

        value = FieldUtils.get_position_close_to_wall_relative_to_own_goal(
            field_length,
            field_width,
            field_goal_width,
            distance,
            distance_to_wall,
            is_left_team,
            upper
        )

        expected_x = 0.75 - distance_to_wall
        expected_y = 0.37 + field_goal_width / 2

        self.assertEqual(value[0], expected_x)
        self.assertEqual(value[1], expected_y)

    def test_get_random_position_at_distance_to_front_line_goal_area(self):
        distance = .2

        field_length = Configuration.get_field_length()
        field_goal_area_length = Configuration.get_field_goal_area_length()
        field_goal_area_width = Configuration.get_field_goal_area_width()
        is_left_team = True

        value = FieldUtils.get_random_position_at_distance_to_front_line_goal_area(
            field_length,
            field_goal_area_length,
            field_goal_area_width,
            distance,
            is_left_team
        )

        print(value)

if __name__ == "__main__":
    unittest.main()