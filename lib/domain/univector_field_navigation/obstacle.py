class Obstacle:
    def __init__(
        self,
        position: 'tuple[float, float]',
        velocities: 'tuple[float, float]' = (0, 0)
    ):
        self.position = position
        self.velocities = velocities
