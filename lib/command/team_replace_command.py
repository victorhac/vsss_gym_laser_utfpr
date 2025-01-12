from lib.command.robot_replace_command import RobotReplaceCommand

class TeamReplaceCommand:
    def __init__(
        self,
        is_yellow_team: bool
    ):
        self.is_yellow_team = is_yellow_team
        self.robot_replace_commands: 'list[RobotReplaceCommand]' = []