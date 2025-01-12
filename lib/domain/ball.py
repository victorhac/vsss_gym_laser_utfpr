from .pose_2d import Pose2D

class Ball:
    def __init__(self):
        self.position = Pose2D()
        self.velocity = Pose2D()

    def __str__(self):
        return (
            f'Position: {self.position}\n'
            f'Velocity: {self.velocity}\n'
        )

    def __repr__(self):
        return f'Ball({self})'
    
    def get_position_tuple(self):
        return (self.position.x, self.position.y)