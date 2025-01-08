from lib.environment.base_environment import BaseEnvironment
from lib.utils.rsoccer_utils import RSoccerUtils
from rsoccer_gym.Entities import Robot
import numpy as np

class EnvironmentUtils:
    @staticmethod
    def get_x_and_y(
        x: float,
        y: float,
        is_left_team: bool
    ):
        if is_left_team:
            return x, y
        return -x, -y
    
    @staticmethod
    def get_norm_theta(robot: Robot, is_left_team: bool):
        if is_left_team:
            return RSoccerUtils.get_corrected_angle(robot.theta) / np.pi
        
        theta = RSoccerUtils.get_corrected_angle(robot.theta)

        if theta < 0:
            theta += np.pi
        elif theta > 0:
            theta -= np.pi

        return theta / np.pi
    
    @staticmethod
    def get_team_and_foe_team(
        environment: BaseEnvironment,
        is_yellow: bool
    ):
        frame = environment.frame

        team = frame.robots_yellow if is_yellow else frame.robots_blue
        foe_team = frame.robots_blue if is_yellow else frame.robots_yellow

        return team, foe_team
