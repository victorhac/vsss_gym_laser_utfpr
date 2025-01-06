from stable_baselines3 import PPO
from lib.environment.test_environment import TestEnvironment

from lib.utils.environment.attacker_environment_utils import AttackerEnvironmentUtils
from lib.utils.environment.defender_environment_utils import DefenderEnvironmentUtils
from lib.utils.environment.goalkeeper_environment_utils import GoalkeeperEnvironmentUtils

render_mode = "human"

def load_model(model_path: str):
    from stable_baselines3 import PPO
    return PPO.load(model_path)

def load_attacker_model():
    return load_model("models/attacker/PPO/2024_9_24_14_48_13/PPO_model_task_6_update_117_13999986_steps.zip")

def load_defender_model():
    return load_model("models/defender/PPO/2025_1_3_23_6_42/interrupted_model.zip")

def load_goalkeeper_model():
    return load_model("models/goalkeeper/PPO/2025_1_4_18_57_50/PPO_model_task_1_update_100_102286296_steps.zip")

env = TestEnvironment(render_mode)

attacker_model = load_attacker_model()
defender_model = load_defender_model()
goalkeeper_model = load_goalkeeper_model()

def get_action(model: PPO, robot_id: int, is_yellow: bool, is_left: bool, get_observation_func):
    observation = get_observation_func(env, robot_id, is_yellow, is_left)
    action, _ = model.predict(observation)
    return action

def get_attacker_action(robot_id: int, is_yellow: bool, is_left: bool):
    return get_action(attacker_model, robot_id, is_yellow, is_left, AttackerEnvironmentUtils.get_observation)

def get_defender_action(robot_id: int, is_yellow: bool, is_left: bool):
    return get_action(defender_model, robot_id, is_yellow, is_left, DefenderEnvironmentUtils.get_observation)

def get_goalkeeper_action(robot_id: int, is_yellow: bool, is_left: bool):
    return get_action(goalkeeper_model, robot_id, is_yellow, is_left, GoalkeeperEnvironmentUtils.get_observation)

def get_actions():
    action = []

    action.extend(get_attacker_action(0, False, True))
    action.extend(get_defender_action(1, False, True))
    action.extend(get_goalkeeper_action(2, False, True))

    action.extend(get_attacker_action(0, True, False))
    action.extend(get_defender_action(1, True, False))
    action.extend(get_goalkeeper_action(2, True, False))

    return action

reward_per_step = []

while True:
    obs = env.reset()
    reward = 0
    done = False
    action = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    while not done:
        next_state, reward, done, _, _ = env.step(action)
        env.render()

        reward_per_step.append(reward)
        action = get_actions()

    #input("Continue...")

    reward_per_step.clear()