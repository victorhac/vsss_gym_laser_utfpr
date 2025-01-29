from lib.domain.enums.role_enum import RoleEnum
from lib.environment.team_environment import TeamEnvironment
from lib.utils.behavior.team_behavior_utils import TeamBehaviorUtils
from lib.utils.model_utils import ModelUtils
from lib.utils.roles.team_utils import TeamUtils
import os

render_mode = 'human'

update_count = 100
updates_per_task = 100
games_count = 100
default_threshold = 0.5

task = TeamBehaviorUtils.get_task_4(
    update_count,
    updates_per_task,
    games_count,
    default_threshold
)

model = ModelUtils.get_team_model()
env = TeamEnvironment(task, render_mode)

while True:
    obs = env.reset()
    reward = 0
    done = False
    action = [0, 2, 3]

    while not done:
        next_state, reward, done, _, _ = env.step(action)
        env.render()
        print(reward)
        observation = TeamUtils.get_observation(env, False, True)
        action = model.predict(observation)[0]