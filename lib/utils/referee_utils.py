import json
from google.protobuf.json_format import MessageToJson

from lib.domain.enums.foul_enum import FoulEnum
from lib.domain.enums.half_enum import HalfEnum
from lib.domain.referee_message import RefereeMessage

class RefereeUtils:
    @staticmethod
    def get_referee_message(packet):
        referee_data = json.loads(MessageToJson(packet))
        foul = referee_data['foul']
        team_color = referee_data['teamcolor']
        foul_quadrant = referee_data['foulquadrant']
        timestamp = referee_data['timestamp']
        game_half = referee_data['gameHalf']

        referee_message = RefereeMessage()
        referee_message.foul_enum = RefereeUtils.get_fould_enum(foul)
        referee_message.is_yellow_team = RefereeUtils.get_is_yellow_team(team_color)
        referee_message.foul_quadrant = int(foul_quadrant)
        referee_message.timestamp = float(timestamp)
        referee_message.game_half_enum = RefereeUtils.get_half_enum(game_half)

        return referee_message

    @staticmethod
    def get_fould_enum(value):
        return FoulEnum(int(value))
    
    @staticmethod
    def get_is_yellow_team(value):
        integer_value = int(value)

        if integer_value == 0:
            return False
        if integer_value == 1:
            return True
        return None
    
    @staticmethod
    def get_half_enum(value):
        return HalfEnum(int(value))