from lib.domain.enums.foul_enum import FoulEnum

class GameStateMachineUtils:
    @staticmethod
    def get_foul_enum_name(
        foul_enum: FoulEnum,
        is_team: 'bool | None' = None
    ):
        if is_team is None:
            return foul_enum.name.lower()
        if is_team:
            return f'{foul_enum.name.lower()}_team'
        return f'{foul_enum.name.lower()}_foe_team'

    @staticmethod
    def get_state_name(
        foul_enum: FoulEnum,
        is_yellow: bool | None,
        is_yellow_team: bool
    ):
        foul_enum_name = GameStateMachineUtils.get_foul_enum_name

        if is_yellow is None:
            return foul_enum_name(foul_enum)
        if is_yellow == is_yellow_team:
            return f'{foul_enum_name(foul_enum)}_team'
        return f'{foul_enum_name(foul_enum)}_foe_team'

    @staticmethod
    def get_trigger_name(
        foul_enum: FoulEnum,
        is_trigger_yellow: bool | None = None
    ):
        foul_enum_name = GameStateMachineUtils.get_foul_enum_name

        if is_trigger_yellow is None:
            return foul_enum_name(foul_enum)
        if is_trigger_yellow:
            return f'{foul_enum_name(foul_enum)}_yellow'
        return f'{foul_enum_name(foul_enum)}_blue'
    
    @staticmethod
    def get_trigger_method_name(
        foul_enum: FoulEnum,
        is_yellow_team: bool
    ):
        team_foe_team_foul_enums = [
            FoulEnum.FREE_KICK,
            FoulEnum.GOAL_KICK,
            FoulEnum.KICKOFF,
            FoulEnum.FREE_BALL]
        
        foul_enum_name = GameStateMachineUtils.get_trigger_name

        if foul_enum in team_foe_team_foul_enums:
            return foul_enum_name(foul_enum, is_yellow_team)
        return foul_enum_name(foul_enum)