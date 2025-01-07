from transitions import Machine

from lib.domain.enums.foul_enum import FoulEnum
from lib.domain.referee_message import RefereeMessage
from lib.utils.game_state_machine_utils import GameStateMachineUtils

class GameStateMachineModel():
    def __init__(self, is_yellow_team: bool):
        self.is_yellow_team = is_yellow_team

    def set_state_by_referee_message(self, message: RefereeMessage):
        team_foe_team_foul_enums = [
            FoulEnum.FREE_KICK,
            FoulEnum.GOAL_KICK,
            FoulEnum.KICKOFF,
            FoulEnum.FREE_BALL]
        
        def get_trigger_name(foul_enum, is_yellow_team = None):
            return GameStateMachineUtils.get_trigger_name(
                foul_enum,
                is_yellow_team
            )

        if message.foul_enum in team_foe_team_foul_enums:
            getattr(
                self,
                get_trigger_name(
                    message.foul_enum,
                    message.is_yellow_team
                ),
                None
            )()
        else:
            getattr(
                self,
                get_trigger_name(message.foul_enum),
                None
            )()

class GameStateMachine(Machine):
    def __init__(
        self,
        is_yellow_team: bool
    ):
        self.is_yellow_team = is_yellow_team
        self.initial_state = FoulEnum.HALT

        def foul_enum_name(foul_enum, is_team = None):
            return GameStateMachineUtils.foul_enum_name(
                foul_enum,
                is_team
            )
        
        def get_state_name(is_yellow, foul_enum):
            return GameStateMachineUtils.get_state_name(
                is_yellow,
                foul_enum,
                self.is_yellow_team
            )
        
        def get_trigger_name(foul_enum, is_trigger_yellow = None):
            return GameStateMachineUtils.get_trigger_name(
                foul_enum,
                is_trigger_yellow
            )

        model = GameStateMachineModel()
        states = [
            foul_enum_name(FoulEnum.FREE_KICK, True),
            foul_enum_name(FoulEnum.FREE_KICK, False),
            foul_enum_name(FoulEnum.GOAL_KICK, True),
            foul_enum_name(FoulEnum.GOAL_KICK, False),
            foul_enum_name(FoulEnum.KICKOFF, True),
            foul_enum_name(FoulEnum.KICKOFF, False),
            foul_enum_name(FoulEnum.FREE_BALL, True),
            foul_enum_name(FoulEnum.FREE_BALL, False),
            foul_enum_name(FoulEnum.GAME_ON),
            foul_enum_name(FoulEnum.HALT)
        ]

        def get_state(
            is_yellow: bool,
            foul_enum: FoulEnum
        ):
            return get_state_name(is_yellow, foul_enum, self.is_yellow_team)

        transitions = [
            {
                'trigger': get_trigger_name(FoulEnum.FREE_KICK, True),
                'source': '*',
                'dest': get_state(True, FoulEnum.FREE_KICK)
            },
            {
                'trigger': get_trigger_name(FoulEnum.FREE_KICK, False),
                'source': '*',
                'dest': get_state(False, FoulEnum.FREE_KICK)
            },
            {
                'trigger': get_trigger_name(FoulEnum.GOAL_KICK, True),
                'source': '*',
                'dest': get_state(True, FoulEnum.GOAL_KICK)
            },
            {
                'trigger': get_trigger_name(FoulEnum.GOAL_KICK, False),
                'source': '*',
                'dest': get_state(False, FoulEnum.GOAL_KICK)
            },
            {
                'trigger': get_trigger_name(FoulEnum.KICKOFF, True),
                'source': '*',
                'dest': get_state(True, FoulEnum.KICKOFF)
            },
            {
                'trigger': get_trigger_name(FoulEnum.KICKOFF, False),
                'source': '*',
                'dest': get_state(False, FoulEnum.KICKOFF)
            },
            {
                'trigger': get_trigger_name(FoulEnum.FREE_BALL, True),
                'source': '*',
                'dest': get_state(True, FoulEnum.FREE_BALL)
            },
            {
                'trigger': get_trigger_name(FoulEnum.FREE_BALL, False),
                'source': '*',
                'dest': get_state(False, FoulEnum.FREE_BALL)
            },
            {
                'trigger': get_trigger_name(FoulEnum.GAME_ON),
                'source': '*',
                'dest': foul_enum_name(FoulEnum.GAME_ON)
            },
            {
                'trigger': get_trigger_name(FoulEnum.HALT),
                'source': '*',
                'dest': foul_enum_name(FoulEnum.HALT)
            },
        ]

        super(GameStateMachine, self).__init__(
            model=model,
            states=states,
            transitions=transitions,
            initial=foul_enum_name(self.initial_state)
        )
