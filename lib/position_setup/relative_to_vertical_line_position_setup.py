from lib.position_setup.position_setup import PositionSetup
from lib.position_setup.position_setup_args import PositionSetupArgs
from lib.utils.field_utils import FieldUtils

class RelativeToVerticalLinePositionSetup(PositionSetup):
    def __init__(
        self,
        is_left_team: bool,
        x_line: float,
        y_range: 'tuple[float, float]',
        left_to_line: bool
    ):
        self.is_left_team = is_left_team
        self.x_line = x_line
        self.y_range = y_range
        self.left_to_line = left_to_line

    def get_position_function(self, args: PositionSetupArgs):
        return lambda: FieldUtils.get_random_position_at_distance_to_vertical_line(
            args.distance,
            self.x_line,
            self.y_range,
            self.left_to_line,
            self.is_left_team)
