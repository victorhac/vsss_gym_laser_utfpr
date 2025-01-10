from communication.receiver.firasim_receiver import FirasimReceiver
from communication.referee.referee import Referee
from communication.sender.firasim_sender import FirasimSender
from configuration.configuration import Configuration
from lib.command.robot_command import RobotCommand
from lib.command.team_command import TeamCommand
from lib.domain.enums.foul_enum import FoulEnum
from lib.domain.field import Field
from lib.domain.referee_message import RefereeMessage
from lib.domain.robot import Robot
from lib.state_machine.game_state_machine import GameStateMachine
from lib.utils.configuration_utils import ConfigurationUtils
from lib.utils.geometry_utils import GeometryUtils
from lib.utils.motion_utils import MotionUtils
from lib.utils.roles.attacker_utils import AttackerUtils
from lib.utils.roles.defender_utils import DefenderUtils
from lib.utils.roles.goalkeeper_utils import GoalkeeperUtils
from lib.utils.game_state_machine_utils import GameStateMachineUtils
from stable_baselines3 import PPO

def load_model(model_path: str):
    return PPO.load(model_path)

def load_attacker_model():
    return load_model(Configuration.model_attacker_path)

def load_defender_model():
    return load_model(Configuration.model_defender_path)

def load_goalkeeper_model():
    return load_model(Configuration.model_goalkeeper_path)

def is_left_team(is_yellow_team: bool):
    return Configuration.firasim_team_is_yellow_left_team == is_yellow_team

def normal_play(is_yellow_team: bool, field: Field):
    left_team = is_left_team(is_yellow_team)
    robot_commands = []

    def get_speeds(get_speeds_function, id, model):
        return get_speeds_function(
            field,
            id,
            left_team,
            model
        )
    
    values = [
        (AttackerUtils.get_speeds_by_field, 0, attacker_model),
        (DefenderUtils.get_speeds_by_field, 1, defender_model),
        (GoalkeeperUtils.get_speeds_by_field, 2, goalkeeper_model),
    ]

    for item in values:
        robot_commands.append(RobotCommand(*get_speeds(*item)))

    command = TeamCommand(is_yellow_team)
    command.commands = robot_commands

    return command

def stopped_play(is_yellow_team: bool):
    command = TeamCommand(is_yellow_team)
    command.commands = [RobotCommand(0, 0) for _ in range(3)]
    return command

def go_to_point_command(
    robot: Robot,
    point: 'tuple[float, float]',
    last_error: int = 0
):
    if GeometryUtils.is_close(
        robot.get_position_tuple(),
        point,
        .05
    ):
        return RobotCommand(0, 0), None
        
    left_speed, right_speed, last_error = MotionUtils.go_to_point(
        robot,
        point,
        last_error,
        Configuration.firasim_robot_speed_max_radians_seconds
    )

    return RobotCommand(left_speed, right_speed), last_error

def positioning(
    positionings: dict,
    is_yellow_team: bool,
    field: Field
):
    robot_commands = []

    for item in positionings:
        if item == "ball":
            continue
        
        robot = field.robots[int(item)]
        robot_command, last_error = go_to_point_command(
            robot,
            (positionings[item]["x"], positionings[item]["y"]),
            0
        )
        robot_commands.append(robot_command)

    command = TeamCommand(is_yellow_team)
    command.commands = robot_commands

    return command

def perform(
    is_yellow_team: bool,
    field: Field,
    message: RefereeMessage,
    machine: GameStateMachine
):
    machine.set_state_by_referee_message(message)
    state = machine.get_state()
    is_left_team = Configuration.firasim_team_is_yellow_left_team == is_yellow_team
    
    def get_state_name(
        foul_enum: FoulEnum,
        is_yellow: 'bool | None' = None
    ):
        return GameStateMachineUtils.get_state_name(
            foul_enum,
            is_yellow,
            is_yellow_team
        )

    if state == get_state_name(FoulEnum.FREE_KICK, is_yellow_team):
        free_kick_team(is_yellow_team, is_left_team, field)
    elif state == get_state_name(FoulEnum.FREE_KICK, not is_yellow_team):
        free_kick_foe_team(is_yellow_team, is_left_team, field)
    elif state == get_state_name(FoulEnum.GOAL_KICK, is_yellow_team):
        goal_kick_team(is_yellow_team, is_left_team, field)
    elif state == get_state_name(FoulEnum.GOAL_KICK, not is_yellow_team):
        goal_kick_foe_team(is_yellow_team, is_left_team, field)
    elif state == get_state_name(FoulEnum.KICKOFF, is_yellow_team):
        kickoff_team(is_yellow_team, is_left_team, field)
    elif state == get_state_name(FoulEnum.KICKOFF, not is_yellow_team):
        kickoff_foe_team(is_yellow_team, is_left_team, field)
    elif state == get_state_name(FoulEnum.FREE_BALL):
        free_ball(is_yellow_team, is_left_team, field, message)
    elif state == get_state_name(FoulEnum.STOP):
        stop(is_yellow_team)
    elif state == get_state_name(FoulEnum.GAME_ON):
        game_on(is_yellow_team, field)
    elif state == get_state_name(FoulEnum.HALT):
        halt(is_yellow_team)
    else:
        halt(is_yellow_team)

def free_kick_team(
    is_yellow_team: bool,
    is_left_team: bool,
    field: Field
):
    positionings = ConfigurationUtils.get_game_states_free_kick_team_positionings(is_left_team)
    return positioning(
        positionings,
        is_yellow_team,
        field
    )

def free_kick_foe_team(
    is_yellow_team: bool,
    is_left_team: bool,
    field: Field
):
    positionings = ConfigurationUtils.get_game_states_free_kick_foe_team_positionings(is_left_team)
    return positioning(
        positionings,
        is_yellow_team,
        field
    )

def goal_kick_team(
    is_yellow_team: bool,
    is_left_team: bool,
    field: Field
):
    positionings = ConfigurationUtils.get_game_states_goal_kick_team_positionings(is_left_team)
    return positioning(
        positionings,
        is_yellow_team,
        field
    )

def goal_kick_foe_team(
    is_yellow_team: bool,
    is_left_team: bool,
    field: Field
):
    positionings = ConfigurationUtils.get_game_states_goal_kick_foe_team_positionings(is_left_team)
    return positioning(
        positionings,
        is_yellow_team,
        field
    )

def free_ball(
    is_yellow_team: bool,
    is_left_team: bool,
    field: Field,
    message: RefereeMessage
):
    positionings = ConfigurationUtils.get_game_states_free_ball_team_positionings(
        is_left_team,
        message.foul_quadrant
    )

    return positioning(
        positionings,
        is_yellow_team,
        field
    )

def kickoff_team(
    is_yellow_team: bool,
    is_left_team: bool,
    field: Field
):
    positionings = ConfigurationUtils.get_game_states_kickoff_team_positionings(is_left_team)
    return positioning(
        positionings,
        is_yellow_team,
        field
    )

def kickoff_foe_team(
    is_yellow_team: bool,
    is_left_team: bool,
    field: Field
):
    positionings = ConfigurationUtils.get_game_states_kickoff_foe_team_positionings(is_left_team)
    return positioning(
        positionings,
        is_yellow_team,
        field
    )

def stop(
    is_yellow_team: bool
):
    return stopped_play(is_yellow_team)

def game_on(
    is_yellow_team: bool,
    field: Field
):
    return normal_play(is_yellow_team, field)

def halt(
    is_yellow_team: bool
):
    return stopped_play(is_yellow_team)

attacker_model = load_attacker_model()
defender_model = load_defender_model()
goalkeeper_model = load_goalkeeper_model()

def main():
    blue_field = Field()
    blue_receiver = FirasimReceiver(blue_field)
    yellow_field = Field()
    yellow_receiver = FirasimReceiver(yellow_field)

    blue_machine = GameStateMachine(False)
    yellow_machine = GameStateMachine(True)

    referee = Referee()
    sender = FirasimSender()

    while True:
        message = referee.receive()
        blue_receiver.update()
        yellow_receiver.update()

        perform(
            False,
            blue_field,
            message,
            blue_machine
        )

        perform(
            True,
            yellow_field,
            message,
            yellow_machine
        )

if __name__ == '__main__':
    main()