class PositionSetupArgs:
    def __init__(
        self,
        distance: 'float | None' = None,
        relative_position: 'tuple[float, float] | None' = None
    ):
        self.distance = distance
        self.position = relative_position
