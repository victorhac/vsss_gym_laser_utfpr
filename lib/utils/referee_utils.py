import json
from google.protobuf.json_format import MessageToJson
from communication.protobuf.referee import vssref_common_pb2
from lib.domain.enums.foul_enum import FoulEnum
from lib.domain.enums.half_enum import HalfEnum
from lib.domain.referee_message import RefereeMessage

class RefereeUtils:
    @staticmethod
    def set_referee_message(referee_message: RefereeMessage, packet):
        referee_data: dict = json.loads(MessageToJson(packet))
        foul = referee_data.get('foul', None)
        team_color = referee_data.get('teamcolor', None)
        foul_quadrant = referee_data.get('foulquadrant', None)
        timestamp = referee_data.get('timestamp', None)
        game_half = referee_data.get('gameHalf', None)

        referee_message.foul_enum = RefereeUtils.get_fould_enum(foul)
        referee_message.is_yellow_team = RefereeUtils.get_is_yellow_team(team_color)
        referee_message.foul_quadrant = None if foul_quadrant is None else int(foul_quadrant)
        referee_message.timestamp = None if timestamp is None else float(timestamp)
        referee_message.game_half_enum = RefereeUtils.get_half_enum(game_half)

    @staticmethod
    def get_fould_enum(value):
        if value is None:
            return None
        return FoulEnum[value]

    @staticmethod
    def get_is_yellow_team(value):
        if value is None:
            return None

        if value == "YELLOW":
            return False
        if value == "BLUE":
            return True

        return True
    
    @staticmethod
    def get_half_enum(value):
        if value is None:
            return None

        return HalfEnum[value]
    
    @staticmethod
    def get_protobuf_color_enum(is_yellow_team: 'bool | None'):
        if is_yellow_team is None:
            return vssref_common_pb2.Color.NONE
        if is_yellow_team:
            return vssref_common_pb2.Color.YELLOW
        return vssref_common_pb2.Color.BLUE
