from stable_baselines3 import PPO
import uuid
from configuration.configuration import Configuration

def _load_ppo_model(model_path: str):
    return PPO.load(model_path)

def _get_attacker_model():
    return _load_ppo_model(Configuration.model_attacker_path)

def _get_defender_model():
    return _load_ppo_model(Configuration.model_defender_path)

def _get_goalkeeper_model():
    return _load_ppo_model(Configuration.model_goalkeeper_path)

def _get_team_model():
    return _load_ppo_model(Configuration.model_team_path)

class StoredModel:
    def __init__(self):
        self.path: str = None
        self.model: PPO = None

class ModelUtils:
    _attacker_model = None
    _defender_model = None
    _goalkeeper_model = None
    _team_model = None
    _model_dictionary: 'dict[str, StoredModel]' = {}

    @staticmethod
    def attacker_model():
        if ModelUtils._attacker_model is None:
            ModelUtils._attacker_model = _get_attacker_model()
        return ModelUtils._attacker_model
    
    @staticmethod
    def defender_model():
        if ModelUtils._defender_model is None:
            ModelUtils._defender_model = _get_defender_model()
        return ModelUtils._defender_model
    
    @staticmethod
    def goalkeeper_model():
        if ModelUtils._goalkeeper_model is None:
            ModelUtils._goalkeeper_model = _get_goalkeeper_model()
        return ModelUtils._goalkeeper_model

    @staticmethod
    def team_model():
        if ModelUtils._team_model is None:
            ModelUtils._team_model = _get_team_model()
        return ModelUtils._team_model
    
    @staticmethod
    def get_id():
        id = str(uuid.uuid4())
        ModelUtils._model_dictionary[id] = StoredModel()
        return id
    
    @staticmethod
    def get_model(
        id: str,
        path: str 
    ):
        item = ModelUtils._model_dictionary.get(id, None)

        if item is None:
            return None

        if item.path != path:
            item.path = path
            item.model = _load_ppo_model(path)

        return item.model
