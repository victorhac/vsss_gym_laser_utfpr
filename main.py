from communication.receiver.firasim_receiver import FirasimReceiver
from communication.referee.referee import Referee
from communication.sender.firasim_sender import FirasimSender
from configuration.configuration import Configuration
from lib.command.robot_command import RobotCommand
from lib.command.team_command import TeamCommand
from lib.domain.enums.foul_enum import FoulEnum
from lib.domain.field import Field
from lib.domain.referee_message import RefereeMessage
from lib.state_machine.game_state_machine import GameStateMachine
from lib.utils.roles.attacker_utils import AttackerUtils
from lib.utils.roles.defender_utils import DefenderUtils
from lib.utils.roles.goalkeeper_utils import GoalkeeperUtils
from lib.utils.game_state_machine_utils import GameStateMachineUtils
from stable_baselines3 import PPO

def load_model(model_path: str):
    return PPO.load(model_path)

def load_attacker_model():
    return load_model("models/attacker/PPO/2024_9_24_14_48_13/PPO_model_task_6_update_117_13999986_steps.zip")

def load_defender_model():
    return load_model("models/defender/PPO/2025_1_3_23_6_42/interrupted_model.zip")

def load_goalkeeper_model():
    return load_model("models/goalkeeper/PPO/2025_1_4_18_57_50/PPO_model_task_1_update_100_102286296_steps.zip")

def is_left_team(is_yellow_team: bool):
    return Configuration.get_firasim_is_left_team() == is_yellow_team

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
        robot_commands.append(get_speeds(*item))

    command = TeamCommand(is_yellow_team)
    command.commands = robot_commands

    return command

def stopped_play():
    pass

attacker_model = load_attacker_model()
defender_model = load_defender_model()
goalkeeper_model = load_goalkeeper_model()

def perform(
    is_yellow_team: bool,
    field: Field,
    message: RefereeMessage,
    machine: GameStateMachine
):
    machine.set_state_by_referee_message(message)
    state = machine.get_state()
    
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
        free_kick_team(is_yellow_team, field, message)
    elif state == get_state_name(FoulEnum.FREE_KICK, not is_yellow_team):
        free_kick_foe_team(is_yellow_team, field, message)
    elif state == get_state_name(FoulEnum.GOAL_KICK, is_yellow_team):
        goal_kick_team(is_yellow_team, field, message)
    elif state == get_state_name(FoulEnum.GOAL_KICK, not is_yellow_team):
        goal_kick_foe_team(is_yellow_team, field, message)
    elif state == get_state_name(FoulEnum.FREE_BALL, is_yellow_team):
        free_ball_team(is_yellow_team, field, message)
    elif state == get_state_name(FoulEnum.FREE_BALL, not is_yellow_team):
        free_ball_foe_team(is_yellow_team, field, message)
    elif state == get_state_name(FoulEnum.KICKOFF, is_yellow_team):
        kickoff_team(is_yellow_team, field, message)
    elif state == get_state_name(FoulEnum.KICKOFF, not is_yellow_team):
        kickoff_foe_team(is_yellow_team, field, message)
    elif state == get_state_name(FoulEnum.STOP):
        stop(is_yellow_team, field, message)
    elif state == get_state_name(FoulEnum.GAME_ON):
        game_on(is_yellow_team, field, message)
    elif state == get_state_name(FoulEnum.HALT):
        halt(is_yellow_team, field, message)
    else:
        halt(is_yellow_team, field, message)

def free_kick_team(
    is_yellow_team: bool,
    field: Field,
    message: RefereeMessage
):
    pass

def free_kick_foe_team(
    is_yellow_team: bool,
    field: Field,
    message: RefereeMessage
):
    pass

def goal_kick_team(
    is_yellow_team: bool,
    field: Field,
    message: RefereeMessage
):
    pass

def goal_kick_foe_team(
    is_yellow_team: bool,
    field: Field,
    message: RefereeMessage
):
    pass

def free_ball_team(
    is_yellow_team: bool,
    field: Field,
    message: RefereeMessage
):
    pass

def free_ball_foe_team(
    is_yellow_team: bool,
    field: Field,
    message: RefereeMessage
):
    pass

def kickoff_team(
    is_yellow_team: bool,
    field: Field,
    message: RefereeMessage
):
    pass

def kickoff_foe_team(
    is_yellow_team: bool,
    field: Field,
    message: RefereeMessage
):
    pass

def stop(
    is_yellow_team: bool,
    field: Field,
    message: RefereeMessage
):
    return stopped_play(is_yellow_team, field)

def game_on(
    is_yellow_team: bool,
    field: Field,
    message: RefereeMessage
):
    return normal_play(is_yellow_team, field)

def halt(
    is_yellow_team: bool,
    field: Field,
    message: RefereeMessage
):
    return stopped_play(is_yellow_team, field)

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