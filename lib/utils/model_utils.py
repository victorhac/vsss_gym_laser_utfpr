from stable_baselines3 import PPO

from configuration.configuration import Configuration

class ModelUtils:
    @staticmethod
    def _load_ppo_model(model_path: str):
        return PPO.load(model_path)
 
    @staticmethod
    def get_attacker_model():
        return ModelUtils._load_ppo_model(Configuration.model_attacker_path)
    
    @staticmethod
    def get_defender_model():
        return ModelUtils._load_ppo_model(Configuration.model_defender_path)
    
    @staticmethod
    def get_goalkeeper_model():
        return ModelUtils._load_ppo_model(Configuration.model_goalkeeper_path)
    
    @staticmethod
    def get_team_model():
        return ModelUtils._load_ppo_model(Configuration.model_team_path)