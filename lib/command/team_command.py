from .robot_command import RobotCommand

class TeamCommand(object):
    def __init__(self, is_yellow: bool):
        self.is_yellow = is_yellow
        self.commands = [RobotCommand() for i in range(3)]

    def reset(self):
        for item in self.commands:
            item.left_speed = 0
            item.right_speed = 0

    def __str__(self):
        message = f'\nTEAM COMMAND:\n'
        for i in range(3):
            message += f'ROBOT_{i}\n{self.commands[i]}'
        return message

    def __repr__(self):
        return f'TeamCommand({self})'