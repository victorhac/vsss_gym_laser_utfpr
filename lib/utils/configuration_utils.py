from configuration.configuration import Configuration

class ConfigurationUtils:
    @staticmethod
    def get_game_states_free_kick_team_positionings():
        return Configuration.game_states_free_kick_team_positionings
    
    @staticmethod
    def get_game_states_free_kick_foe_team_positionings():
        return Configuration.game_states_free_kick_foe_team_positionings
    
    @staticmethod
    def get_game_states_penalty_kick_team_positionings():
        return Configuration.game_states_penalty_kick_team_positionings
    
    @staticmethod
    def get_game_states_penalty_kick_foe_team_positionings():
        return Configuration.game_states_penalty_kick_foe_team_positionings
        
    @staticmethod
    def get_game_states_goal_kick_team_positionings():
        return Configuration.game_states_goal_kick_team_positionings
    
    @staticmethod
    def get_game_states_goal_kick_foe_team_positionings():
        return Configuration.game_states_goal_kick_foe_team_positionings
    
    @staticmethod
    def get_game_states_kickoff_team_positionings():
        return Configuration.game_states_kickoff_team_positionings
    
    @staticmethod
    def get_game_states_kickoff_foe_team_positionings():
        return Configuration.game_states_kickoff_foe_team_positionings
    
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
            return Configuration.game_states_free_ball_quadrant_1_positionings
    
        return Configuration.game_states_free_ball_quadrant_3_positionings
    
    @staticmethod
    def get_game_states_free_ball_team_quadrant_2_positionings(is_left_team: bool):
        if is_left_team:
            return Configuration.game_states_free_ball_quadrant_2_positionings

        return Configuration.game_states_free_ball_quadrant_4_positionings
    
    @staticmethod
    def get_game_states_free_ball_team_quadrant_3_positionings(is_left_team: bool):
        if is_left_team:
            return Configuration.game_states_free_ball_quadrant_3_positionings

        return Configuration.game_states_free_ball_quadrant_1_positionings
    
    @staticmethod
    def get_game_states_free_ball_team_quadrant_4_positionings(is_left_team: bool):
        if is_left_team:
            return Configuration.game_states_free_ball_quadrant_4_positionings

        return Configuration.game_states_free_ball_quadrant_2_positionings
