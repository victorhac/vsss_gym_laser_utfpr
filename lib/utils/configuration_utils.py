from configuration.configuration import Configuration

class ConfigurationUtils:
    @staticmethod
    def _convert_positionings_when_right_team(positionings: dict):
        for item in positionings:
            positionings[item]["x"] = -positionings[item]["x"]
            positionings[item]["y"] = -positionings[item]["y"]

    @staticmethod
    def get_game_states_free_kick_team_positionings(is_left_team: bool):
        positionings = Configuration.game_states_free_kick_team_positionings.copy()

        if not is_left_team:
            ConfigurationUtils._convert_positionings_when_right_team(positionings)

        return positionings
    
    @staticmethod
    def get_game_states_free_kick_foe_team_positionings(is_left_team: bool):
        positionings = Configuration.game_states_free_kick_foe_team_positionings.copy()

        if not is_left_team:
            ConfigurationUtils._convert_positionings_when_right_team(positionings)

        return positionings
    
    @staticmethod
    def get_game_states_penalty_kick_team_positionings(is_left_team: bool):
        positionings = Configuration.game_states_penalty_kick_team_positionings.copy()

        if not is_left_team:
            ConfigurationUtils._convert_positionings_when_right_team(positionings)

        return positionings
    
    @staticmethod
    def get_game_states_penalty_kick_foe_team_positionings(is_left_team: bool):
        positionings = Configuration.game_states_penalty_kick_foe_team_positionings.copy()

        if not is_left_team:
            ConfigurationUtils._convert_positionings_when_right_team(positionings)

        return positionings
        
    @staticmethod
    def get_game_states_goal_kick_team_positionings(is_left_team: bool):
        positionings = Configuration.game_states_goal_kick_team_positionings.copy()

        if not is_left_team:
            ConfigurationUtils._convert_positionings_when_right_team(positionings)

        return positionings
    
    @staticmethod
    def get_game_states_goal_kick_foe_team_positionings(is_left_team: bool):
        positionings = Configuration.game_states_goal_kick_foe_team_positionings.copy()

        if not is_left_team:
            ConfigurationUtils._convert_positionings_when_right_team(positionings)

        return positionings
    
    @staticmethod
    def get_game_states_kickoff_team_positionings(is_left_team: bool):
        positionings = Configuration.game_states_kickoff_team_positionings.copy()

        if not is_left_team:
            ConfigurationUtils._convert_positionings_when_right_team(positionings)

        return positionings
    
    @staticmethod
    def get_game_states_kickoff_foe_team_positionings(is_left_team: bool):
        positionings = Configuration.game_states_kickoff_foe_team_positionings.copy()

        if not is_left_team:
            ConfigurationUtils._convert_positionings_when_right_team(positionings)

        return positionings
    
    @staticmethod
    def get_game_states_free_ball_team_positionings(is_left_team: bool, quadrant: int):
        if quadrant == 1:
            return ConfigurationUtils.get_game_states_free_ball_team_quadrant_1_positionings(is_left_team)
        if quadrant == 2:
            return ConfigurationUtils.get_game_states_free_ball_team_quadrant_2_positionings(is_left_team)
        if quadrant == 3:
            return ConfigurationUtils.get_game_states_free_ball_team_quadrant_3_positionings(is_left_team)
        return ConfigurationUtils.get_game_states_free_ball_team_quadrant_4_positionings(is_left_team)

    @staticmethod
    def get_game_states_free_ball_team_quadrant_1_positionings(is_left_team: bool):
        if is_left_team:
            return Configuration.game_states_free_ball_quadrant_1_positionings.copy()

        positionings = Configuration.game_states_free_ball_quadrant_3_positionings.copy()
        ConfigurationUtils._convert_positionings_when_right_team(positionings)
        return positionings
    
    @staticmethod
    def get_game_states_free_ball_team_quadrant_2_positionings(is_left_team: bool):
        if is_left_team:
            return Configuration.game_states_free_ball_quadrant_2_positionings.copy()

        positionings = Configuration.game_states_free_ball_quadrant_4_positionings.copy()
        ConfigurationUtils._convert_positionings_when_right_team(positionings)
        return positionings
    
    @staticmethod
    def get_game_states_free_ball_team_quadrant_3_positionings(is_left_team: bool):
        if is_left_team:
            return Configuration.game_states_free_ball_quadrant_3_positionings.copy()

        positionings = Configuration.game_states_free_ball_quadrant_1_positionings.copy()
        ConfigurationUtils._convert_positionings_when_right_team(positionings)
        return positionings
    
    @staticmethod
    def get_game_states_free_ball_team_quadrant_4_positionings(is_left_team: bool):
        if is_left_team:
            return Configuration.game_states_free_ball_quadrant_4_positionings.copy()

        positionings = Configuration.game_states_free_ball_quadrant_2_positionings.copy()
        ConfigurationUtils._convert_positionings_when_right_team(positionings)
        return positionings
