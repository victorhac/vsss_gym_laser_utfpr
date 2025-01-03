import unittest

from lib.utils.geometry_utils import GeometryUtils

class TestGeometryUtils(unittest.TestCase):
    def test_get_position_close_to_wall_relative_to_own_goal(self):
        current_position = (-.1, .3)
        ball_position = (0, .3)
        left_wall_position = (-.75, ball_position[1])

        position = GeometryUtils.closest_point_on_line_segment(
            current_position,
            left_wall_position,
            ball_position
        )

        print(position)

if __name__ == "__main__":
    unittest.main()