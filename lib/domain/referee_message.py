from lib.domain.enums.foul_enum import FoulEnum
from lib.domain.enums.half_enum import HalfEnum

class RefereeMessage:
    foul_enum: FoulEnum = None
    is_yellow_team: bool = None
    game_half_enum: HalfEnum = None
    foul_quadrant: int = None
    timestamp: float = None