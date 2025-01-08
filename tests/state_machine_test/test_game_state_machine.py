import unittest

from lib.domain.enums.foul_enum import FoulEnum
from lib.domain.referee_message import RefereeMessage
from lib.state_machine.game_state_machine import GameStateMachine

class TestGameStateMachine(unittest.TestCase):
    def should_all_run_when_is_free_ball_foe_team(self):
        is_yellow_team = False
        machine = GameStateMachine(is_yellow_team)
        message = RefereeMessage()

        message.foul_enum = FoulEnum.FREE_BALL
        message.is_yellow_team = True

        machine.set_state_by_referee_message(message)

        self.assertEqual(machine.get_state(), 'free_ball_foe_team')

    def should_all_run_when_is_free_kick_team(self):
        is_yellow_team = True
        machine = GameStateMachine(is_yellow_team)
        message = RefereeMessage()

        message.foul_enum = FoulEnum.FREE_KICK
        message.is_yellow_team = is_yellow_team

        machine.set_state_by_referee_message(message)

        self.assertEqual(machine.get_state(), 'free_kick_team')
