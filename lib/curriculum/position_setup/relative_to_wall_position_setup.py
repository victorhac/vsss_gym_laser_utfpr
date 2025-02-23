import random
from configuration.configuration import Configuration
from lib.curriculum.position_setup.position_setup import PositionSetup
from lib.domain.position_setup_args import PositionSetupArgs
from lib.utils.field_utils import FieldUtils

class RelativeToWallPositionSetup(PositionSetup):
    def __init__(
        self,
        is_left_team: bool,
        distance_to_wall: float
    ):
        self.is_left_team = is_left_team
        self.distance_to_wall = distance_to_wall

    def get_position_function(self, args: PositionSetupArgs):
        upper = random.choice([True, False])

        return lambda: FieldUtils.get_position_close_to_wall_relative_to_own_goal(
            Configuration.field_length,
            Configuration.field_width,
            Configuration.field_goal_width,
            args.distance,
            self.distance_to_wall,
            self.is_left_team,
            upper)
