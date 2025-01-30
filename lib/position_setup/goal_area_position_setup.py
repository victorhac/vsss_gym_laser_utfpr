from configuration.configuration import Configuration
from lib.position_setup.position_setup import PositionSetup
from lib.utils.field_utils import FieldUtils

class GoalAreaPositionSetup(PositionSetup):
    def __init__(self, is_left_team: bool):
        self.is_left_team = is_left_team

    def get_position_function(self, args = None):
        return lambda: FieldUtils.get_random_position_inside_own_goal_area(
            Configuration.field_length,
            Configuration.field_goal_area_length,
            Configuration.field_goal_area_width,
            self.is_left_team)
