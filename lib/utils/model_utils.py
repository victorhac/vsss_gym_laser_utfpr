from stable_baselines3 import PPO

class ModelUtils:
    @staticmethod
    def _load_ppo_model(model_path: str):
        return PPO.load(model_path)

    @staticmethod
    def get_attacker_model():
        return ModelUtils._load_ppo_model("models/attacker/PPO/2024_9_24_14_48_13/PPO_model_task_6_update_117_13999986_steps.zip")
    
    @staticmethod
    def get_defender_model():
        return ModelUtils._load_ppo_model("models/defender/PPO/2025_1_3_23_6_42/interrupted_model.zip")
    
    @staticmethod
    def get_goalkeeper_model():
        return ModelUtils._load_ppo_model("models/goalkeeper/PPO/2025_1_25_18_2_1/PPO_model_task_1_update_100_36667946_steps.zip")