import unittest

from configuration.configuration import Configuration
from lib.utils.field_utils import FieldUtils

class TestFieldUtils(unittest.TestCase):
    def test_get_position_close_to_wall_relative_to_own_goal(self):
        field_length = Configuration.get_field_length()
        field_width = Configuration.get_field_width()
        field_goal_width = Configuration.get_field_goal_width()
        goal_position = FieldUtils.get_own_goal_position(field_length, False)

        distance = 2.05
        distance_to_wall = .2
        is_left_team = False
        is_yellow = True

        value = FieldUtils.get_position_close_to_wall_relative_to_own_goal(
            field_length,
            field_width,
            field_goal_width,
            distance,
            distance_to_wall,
            is_left_team,
            is_yellow
        )

        self.assertEqual(value[0], -(goal_position[0] - distance_to_wall))
        self.assertEqual(value[1], -0.55)

if __name__ == "__main__":
    pass