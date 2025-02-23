from .pose_2d import Pose2D

class Robot():
    def __init__(self, id, active):
        self.id = id
        self.active = active
        self.position = Pose2D()
        self.velocity = Pose2D()

    def __str__(self):
        return (
            f'Position: {self.position}\n'
            f'Velocity: {self.velocity}\n'
        )

    def __repr__(self):
        return f'Robot({self})'
    
    def get_position_tuple(self):
        return (self.position.x, self.position.y)
    
    def get_velocity_tuple(self):
        return (self.velocity.x, self.velocity.y)