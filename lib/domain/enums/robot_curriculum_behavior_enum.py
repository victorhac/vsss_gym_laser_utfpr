from enum import Enum

class RobotCurriculumBehaviorEnum(Enum):
    NONE = 0
    BALL_FOLLOWING = 1
    GOALKEEPER_BALL_FOLLOWING = 2
    FROM_PREVIOUS_MODEL = 3,
    FROM_FIXED_MODEL = 4,
    FROM_MODEL = 5
    MULTIPLE_ROLE = 6