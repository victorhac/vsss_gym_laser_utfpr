from lib.position_setup.position_setup import PositionSetup

class FixedPositionSetup(PositionSetup):
    def __init__(
        self,
        position: 'tuple[float, float]'
    ):
        self.position = position

    def get_position_function(self, args = None):
        return lambda: self.position
