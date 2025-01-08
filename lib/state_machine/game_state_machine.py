from transitions import Machine

from lib.domain.enums.foul_enum import FoulEnum
from lib.domain.referee_message import RefereeMessage
from lib.utils.game_state_machine_utils import GameStateMachineUtils

class GameStateMachineModel():
    def set_state_by_referee_message(
        self,
        message: RefereeMessage
    ):        
        get_trigger_name = GameStateMachineUtils.get_trigger_method_name(
            message.foul_enum,
            message.is_yellow_team
        )

        getattr(
            self,
            get_trigger_name,
            None
        )()

class GameStateMachine:
    def __init__(
        self,
        is_yellow_team: bool
    ):
        self.model = GameStateMachineModel()
        self.is_yellow_team = is_yellow_team
        self.initial_state = FoulEnum.HALT

        get_foul_enum_name = lambda foul_enum, is_team = None:\
            GameStateMachineUtils.get_foul_enum_name(
                foul_enum,
                is_team
            )
        
        get_state_name = lambda foul_enum, is_yellow:\
            GameStateMachineUtils.get_state_name(
                foul_enum,
                is_yellow,
                self.is_yellow_team
            )
        
        get_trigger_name = lambda foul_enum, is_trigger_yellow = None:\
            GameStateMachineUtils.get_trigger_name(
                foul_enum,
                is_trigger_yellow
            )

        states = [
            get_foul_enum_name(FoulEnum.FREE_KICK, True),
            get_foul_enum_name(FoulEnum.FREE_KICK, False),
            get_foul_enum_name(FoulEnum.GOAL_KICK, True),
            get_foul_enum_name(FoulEnum.GOAL_KICK, False),
            get_foul_enum_name(FoulEnum.KICKOFF, True),
            get_foul_enum_name(FoulEnum.KICKOFF, False),
            get_foul_enum_name(FoulEnum.FREE_BALL, True),
            get_foul_enum_name(FoulEnum.FREE_BALL, False),
            get_foul_enum_name(FoulEnum.GAME_ON),
            get_foul_enum_name(FoulEnum.HALT)
        ]

        transitions = [
            {
                'trigger': get_trigger_name(FoulEnum.FREE_KICK, True),
                'source': '*',
                'dest': get_state_name(FoulEnum.FREE_KICK, True)
            },
            {
                'trigger': get_trigger_name(FoulEnum.FREE_KICK, False),
                'source': '*',
                'dest': get_state_name(FoulEnum.FREE_KICK, False)
            },
            {
                'trigger': get_trigger_name(FoulEnum.GOAL_KICK, True),
                'source': '*',
                'dest': get_state_name(FoulEnum.GOAL_KICK, True)
            },
            {
                'trigger': get_trigger_name(FoulEnum.GOAL_KICK, False),
                'source': '*',
                'dest': get_state_name(FoulEnum.GOAL_KICK, False)
            },
            {
                'trigger': get_trigger_name(FoulEnum.KICKOFF, True),
                'source': '*',
                'dest': get_state_name(FoulEnum.KICKOFF, True)
            },
            {
                'trigger': get_trigger_name(FoulEnum.KICKOFF, False),
                'source': '*',
                'dest': get_state_name(FoulEnum.KICKOFF, False)
            },
            {
                'trigger': get_trigger_name(FoulEnum.FREE_BALL, True),
                'source': '*',
                'dest': get_state_name(FoulEnum.FREE_BALL, True)
            },
            {
                'trigger': get_trigger_name(FoulEnum.FREE_BALL, False),
                'source': '*',
                'dest': get_state_name(FoulEnum.FREE_BALL, False)
            },
            {
                'trigger': get_trigger_name(FoulEnum.GAME_ON),
                'source': '*',
                'dest': get_foul_enum_name(FoulEnum.GAME_ON)
            },
            {
                'trigger': get_trigger_name(FoulEnum.HALT),
                'source': '*',
                'dest': get_foul_enum_name(FoulEnum.HALT)
            },
        ]

        self.machine = Machine(
            model=self.model,
            states=states,
            transitions=transitions,
            initial=get_foul_enum_name(self.initial_state)
        )

    def set_state_by_referee_message(self, message: RefereeMessage):  
        self.model.set_state_by_referee_message(message)

    def get_state(self):
        return self.model.state