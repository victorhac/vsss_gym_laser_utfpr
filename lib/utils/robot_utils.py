class RobotUtils:
    @staticmethod
    def truncate_motor_speed(motorSpeed: float, baseSpeed: float):
        if motorSpeed > baseSpeed:
            motorSpeed = baseSpeed
        elif motorSpeed < -baseSpeed:
            motorSpeed = -baseSpeed
        return motorSpeed