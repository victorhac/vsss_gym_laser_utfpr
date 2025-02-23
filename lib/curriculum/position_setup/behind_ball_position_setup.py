from lib.curriculum.position_setup.position_setup import PositionSetup
from lib.domain.position_setup_args import PositionSetupArgs

class BehindBallPositionSetup(PositionSetup):
    def __init__(self, is_left_team: bool):
        self.is_left_team = is_left_team

    def get_position_function(self, args: PositionSetupArgs):
        return lambda: self._get_position_behind_position(
            args.position,
            args.distance,
            self.is_left_team)
    
    def _get_position_behind_position(
        self,
        position: 'tuple[float, float]',
        distance: float,
        is_left_team: bool
    ):
        if not is_left_team:
            distance = -distance

        x = position[0] - distance
        y = position[1]
        
        return x, y
