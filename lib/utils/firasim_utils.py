import math
import numpy as np

class FIRASimUtils:
    @staticmethod
    def correct_angle(
        angle: float,
        is_left_team: bool
    ):
        sum_to_angle = 0 if not is_left_team else np.pi
        angle = FIRASimUtils._assert_angle(angle + sum_to_angle)

        if angle < 0:
            return angle + math.pi
        elif angle > 0:
            return angle - math.pi
        return angle
    
    @staticmethod
    def _assert_angle(angle: float):
        angle = angle % (2 * np.pi)

        if angle > np.pi:
            angle -= 2 * np.pi

        return angle
    
    @staticmethod
    def correct_position(
        x: float,
        y: float,
        is_left_team: bool):
        
        if is_left_team:
            return x, y 
        
        return -x, -y
    
    @staticmethod
    def correct_speed(
        x: float,
        y: float,
        is_left_team: bool):

        if is_left_team:
            return x, y 
        
        return -x, -y