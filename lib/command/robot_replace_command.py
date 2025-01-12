class RobotReplaceCommand:
    def __init__(
        self,
        robot_id: int,
        x: float,
        y: float,
        theta: float
    ):
        self.robot_id = robot_id
        self.x = x
        self.y = y
        self.theta = theta