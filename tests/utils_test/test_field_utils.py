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

    def test_get_random_position_at_distance_to_vertical_line(self):
        x_line = -.6
        y_range = (-.35, .35)
        left_to_line = False
        is_left_team = True
        distance = .2

        position = FieldUtils.get_random_position_at_distance_to_vertical_line(
            distance,
            x_line,
            y_range,
            left_to_line,
            is_left_team
        )

        print(position)

if __name__ == "__main__":
    unittest.main()