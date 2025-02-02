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
    def get_game_states_free_ball_team_positionings(quadrant: int):
        if quadrant == 1:
            return Configuration.game_states_free_ball_quadrant_1_positionings
        if quadrant == 2:
            return Configuration.game_states_free_ball_quadrant_2_positionings
        if quadrant == 3:
            return Configuration.game_states_free_ball_quadrant_3_positionings

        return Configuration.game_states_free_ball_quadrant_4_positionings
