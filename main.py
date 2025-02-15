import threading
from communication.receiver.firasim_receiver import FirasimReceiver
from communication.referee.referee import Referee
from communication.replacer.replacer import Replacer
from communication.sender.firasim_sender import FirasimSender
from configuration.configuration import Configuration
from lib.command.robot_command import RobotCommand
from lib.command.team_command import TeamCommand
from lib.domain.enums.foul_enum import FoulEnum
from lib.domain.field import Field
from lib.domain.referee_message import RefereeMessage
from lib.domain.robot import Robot
from lib.positioning.default_supporter_positioning import get_supporter_position
from lib.state_machine.game_state_machine import GameStateMachine
from lib.utils.configuration_utils import ConfigurationUtils
from lib.utils.field_utils import FieldUtils
from lib.utils.model_utils import ModelUtils
from lib.utils.motion_utils import MotionUtils
from lib.utils.roles.attacker_utils import AttackerUtils
from lib.utils.roles.defender_utils import DefenderUtils
from lib.utils.roles.goalkeeper_utils import GoalkeeperUtils
from lib.utils.game_state_machine_utils import GameStateMachineUtils
import time

from lib.utils.roles.team_utils import TeamUtils

start_time = time.time()

pid_errors = {
    "True": {
        "0": 0,
        "1": 0,
        "2": 0
    },
    "False": {
        "0": 0,
        "1": 0,
        "2": 0
    }
}

def get_attacker_speeds(
    field: Field,
    robot_id: int
):
    return AttackerUtils.get_speeds_by_field(
        field,
        robot_id,
        attacker_model
    )

def get_defender_speeds(
    field: Field,
    robot_id: int
):
    return DefenderUtils.get_speeds_by_field(
        field,
        robot_id,
        defender_model
    )

def get_goalkeeper_speeds(
    field: Field,
    robot_id: int
):
    return GoalkeeperUtils.get_speeds_by_field(
        field,
        robot_id,
        goalkeeper_model
    )

def get_supporter_speeds(
    field: Field,
    robot_id: int
):
    robot = field.get_robot_by_id(robot_id)
    position = get_supporter_position(robot_id, field)
    obstacles = FieldUtils.to_obstacles_except_current_robot_and_ball(
        field,
        robot_id
    )

    return MotionUtils.go_to_point_univector(
        robot,
        position,
        obstacles
    )

def get_team_actions(field: Field):
    return TeamUtils.get_observation_by_field(field)

def is_left_team(is_yellow_team: bool):
    return Configuration.firasim_team_is_yellow_left_team == is_yellow_team

def team_coordinated_normal_play(field: Field):
    action = TeamUtils.get_action_by_field(
        field,
        team_model,
        start_time
    )

    robot_commands = []

    for i in range(3):
        if action[i] == 0:
            left_speed, right_speed = get_attacker_speeds(field, i)
        elif action[i] == 1:
            left_speed, right_speed = get_defender_speeds(field, i)
        elif action[i] == 2:
            left_speed, right_speed = get_goalkeeper_speeds(field, i)
        else:
            left_speed, right_speed = get_supporter_speeds(field, i)

        robot_commands.append(RobotCommand(left_speed, right_speed))

    return robot_commands

def team_without_coordination_normal_play(field: Field):
    robot_commands = []

    def get_speeds(get_speeds_function, id, model):
        return get_speeds_function(
            field,
            id,
            model
        )
    
    values = [
        (AttackerUtils.get_speeds_by_field, 0, attacker_model),
        (DefenderUtils.get_speeds_by_field, 1, defender_model),
        (GoalkeeperUtils.get_speeds_by_field, 2, goalkeeper_model),
    ]

    for item in values:
        robot_commands.append(RobotCommand(*get_speeds(*item)))

    return robot_commands

def normal_play(
    is_yellow_team: bool,
    field: Field
):
    if Configuration.firasim_team_is_yellow_team == is_yellow_team:
        return team_coordinated_normal_play(field)
    else:
        return team_without_coordination_normal_play(field)

def stopped_play():
    return [RobotCommand(0, 0) for _ in range(3)]

def go_to_point_command(
    robot: Robot,
    field: Field,
    point: 'tuple[float, float]',
    last_error: int = 0
):    
    obstacles = FieldUtils.to_obstacles_except_current_robot(
        field,
        robot.id
    )
    
    left_speed, right_speed = MotionUtils.go_to_point_univector(
        robot,
        point,
        obstacles
    )

    return RobotCommand(left_speed, right_speed), 0

def positioning(
    is_yellow_team: bool,
    positionings: dict,
    field: Field
):
    robot_commands = []

    for item in positionings:
        if item == "ball":
            continue

        robot = field.get_robot_by_id(int(item))

        if robot.active:
            pid_error_key_team = str(is_yellow_team)
            robot_command, pid_errors[pid_error_key_team][item] = go_to_point_command(
                robot,
                field,
                (positionings[item]["x"], positionings[item]["y"]),
                pid_errors[pid_error_key_team][item]
            )

            robot_commands.append(robot_command)

    return robot_commands

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
        commands = free_kick_team(is_yellow_team, is_left_team, field)
    elif state == get_state_name(FoulEnum.FREE_KICK, not is_yellow_team):
        commands = free_kick_foe_team(is_yellow_team, is_left_team, field)
    elif state == get_state_name(FoulEnum.PENALTY_KICK, is_yellow_team):
        commands = penalty_kick_team(is_yellow_team, field)
    elif state == get_state_name(FoulEnum.PENALTY_KICK, not is_yellow_team):
        commands = penalty_kick_foe_team(is_yellow_team, field)
    elif state == get_state_name(FoulEnum.GOAL_KICK, is_yellow_team):
        commands = goal_kick_team(is_yellow_team, field)
    elif state == get_state_name(FoulEnum.GOAL_KICK, not is_yellow_team):
        commands = goal_kick_foe_team(is_yellow_team, field)
    elif state == get_state_name(FoulEnum.KICKOFF, is_yellow_team):
        commands = kickoff_team(is_yellow_team, field)
    elif state == get_state_name(FoulEnum.KICKOFF, not is_yellow_team):
        commands = kickoff_foe_team(is_yellow_team, field)
    elif state == get_state_name(FoulEnum.FREE_BALL):
       commands = free_ball(is_yellow_team, field)
    elif state == get_state_name(FoulEnum.STOP):
        commands = stop()
    elif state == get_state_name(FoulEnum.GAME_ON):
        commands = game_on(is_yellow_team, field)
    elif state == get_state_name(FoulEnum.HALT):
        commands = halt()
    else:
        commands = halt()

    if commands is None:
        return None

    command = TeamCommand(is_yellow_team)
    command.commands = commands

    return command

def free_kick_team(
    is_yellow_team: bool,
    is_left_team: bool,
    field: Field
):
    positionings = ConfigurationUtils.get_game_states_free_kick_team_positionings(is_left_team)
    return positioning(
        is_yellow_team,
        positionings,
        field
    )

def free_kick_foe_team(
    is_yellow_team: bool,
    is_left_team: bool,
    field: Field
):
    positionings = ConfigurationUtils.get_game_states_free_kick_foe_team_positionings(is_left_team)
    return positioning(
        is_yellow_team,
        positionings,
        field
    )

def penalty_kick_team(
    is_yellow_team: bool,
    field: Field
):
    positionings = ConfigurationUtils.get_game_states_penalty_kick_team_positionings()
    return positioning(
        is_yellow_team,
        positionings,
        field
    )

def penalty_kick_foe_team(
    is_yellow_team: bool,
    field: Field
):
    positionings = ConfigurationUtils.get_game_states_penalty_kick_foe_team_positionings()
    return positioning(
        is_yellow_team,
        positionings,
        field
    )

def goal_kick_team(
    is_yellow_team: bool,
    field: Field
):
    positionings = ConfigurationUtils.get_game_states_goal_kick_team_positionings()
    return positioning(
        is_yellow_team,
        positionings,
        field
    )

def goal_kick_foe_team(
    is_yellow_team: bool,
    field: Field
):
    positionings = ConfigurationUtils.get_game_states_goal_kick_foe_team_positionings()
    return positioning(
        is_yellow_team,
        positionings,
        field
    )

def free_ball(
    is_yellow_team: bool,
    field: Field
):
    positionings = ConfigurationUtils.get_game_states_free_ball_team_positionings(
        FieldUtils.get_quadrant_where_ball_is_located(field.ball)
    )

    return positioning(
        is_yellow_team,
        positionings,
        field
    )

def kickoff_team(
    is_yellow_team: bool,
    field: Field
):
    positionings = ConfigurationUtils.get_game_states_kickoff_team_positionings()
    return positioning(
        is_yellow_team,
        positionings,
        field
    )

def kickoff_foe_team(
    is_yellow_team: bool,
    field: Field
):
    positionings = ConfigurationUtils.get_game_states_kickoff_foe_team_positionings()
    return positioning(
        is_yellow_team,
        positionings,
        field
    )

def stop():
    return stopped_play()

def game_on(
    is_yellow_team: bool,
    field: Field
):
    return normal_play(is_yellow_team, field)

def halt():
    return stopped_play()

attacker_model = ModelUtils.attacker_model()
defender_model = ModelUtils.defender_model()
goalkeeper_model = ModelUtils.goalkeeper_model()
team_model = ModelUtils.team_model()

blue_field = Field()
blue_receiver = FirasimReceiver(False, blue_field)
yellow_field = Field()
yellow_receiver = FirasimReceiver(True, yellow_field)

blue_machine = GameStateMachine(False)
yellow_machine = GameStateMachine(True)

referee_message = RefereeMessage()

referee = Referee(referee_message)
sender = FirasimSender()
replacer = Replacer()

def update():
    while True:
        referee.update()
        blue_receiver.update()
        yellow_receiver.update()

update_thread = threading.Thread(target=update)

def main():
    update_thread.start()
    while True:
        blue_command = perform(
            False,
            blue_field,
            referee_message,
            blue_machine
        )

        yellow_command = perform(
            True,
            yellow_field,
            referee_message,
            yellow_machine
        )

        if blue_command is not None:
            sender.transmit_team(blue_command)

        if yellow_command is not None:
            sender.transmit_team(yellow_command)

if __name__ == '__main__':
    main()