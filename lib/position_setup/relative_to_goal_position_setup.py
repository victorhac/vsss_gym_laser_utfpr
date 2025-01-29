from configuration.configuration import Configuration
from lib.position_setup.position_setup import PositionSetup
from lib.position_setup.position_setup_args import PositionSetupArgs
from lib.utils.field_utils import FieldUtils

class RelativeToGoalPositionSetup(PositionSetup):
    def __init__(self, is_left_team: bool):
        self.is_left_team = is_left_team

    def get_position_function(self, args: PositionSetupArgs):
        return lambda: FieldUtils.get_random_position_at_distance(
            Configuration.field_length,
            Configuration.field_width,
            FieldUtils.get_own_goal_position(
                Configuration.field_length,
                self.is_left_team
            ),
            args.distance)
