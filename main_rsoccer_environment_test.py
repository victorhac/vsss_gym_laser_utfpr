from stable_baselines3 import PPO
from lib.domain.enums.role_enum import RoleEnum
from lib.environment.attacker.attacker_v2_environment import AttackerV2Environment
from lib.environment.goalkeeper.goalkeeper_v2_environment import GoalkeeperV2Environment
from lib.environment.team_environment import TeamEnvironment
from lib.utils.behavior.attacker.attacker_v2_behavior_utils import AttackerV2BehaviorUtils
from lib.utils.behavior.goalkeeper.goalkeeper_v2_behavior_utils import GoalkeeperV2BehaviorUtils
from lib.utils.behavior.goalkeeper_behavior_utils import GoalkeeperBehaviorUtils
from lib.utils.behavior.team_behavior_utils import TeamBehaviorUtils
from lib.utils.model_utils import ModelUtils
from lib.utils.roles.attacker.attacker_v2_utils import AttackerV2Utils
from lib.utils.roles.goalkeeper.goalkeeper_v2_utils import GoalkeeperV2Utils
from lib.utils.roles.team_utils import TeamUtils
import os

render_mode = 'human'

update_count = 0
updates_per_task = 2
games_count = 2
default_threshold = 0.5

model = PPO.load("models/goalkeeper_v2/PPO/2025_1_30_17_53_48/PPO_model_task_1_update_0_15999984_steps.zip")

task = GoalkeeperV2BehaviorUtils.get_task_1(
    update_count,
    updates_per_task,
    games_count,
    default_threshold
)

env = GoalkeeperV2Environment(task, render_mode)

while True:
    obs = env.reset()
    reward = 0
    done = False
    action = (0, 0)

    while not done:
        next_state, reward, done, _, _ = env.step(action)
        env.render()
        observation = GoalkeeperV2Utils.get_observation(env, 0, False, True)
        action = model.predict(observation)[0]