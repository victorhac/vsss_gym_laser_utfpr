from lib.domain.enums.role_enum import RoleEnum
from lib.environment.team_environment import TeamEnvironment
from lib.utils.behavior.team_behavior_utils import TeamBehaviorUtils
from lib.utils.model_utils import ModelUtils
from lib.utils.roles.team_utils import TeamUtils

render_mode = 'human'

update_count = 3
updates_per_task = 3
games_count = 100
default_threshold = 0.5

task = TeamBehaviorUtils.get_task_2(
    update_count,
    updates_per_task,
    games_count,
    default_threshold
)

env = TeamEnvironment(task, render_mode)

while True:
    obs = env.reset()
    reward = 0
    done = False
    action = [1, 2, 4]

    while not done:
        next_state, reward, done, _, _ = env.step(action)
        env.render()
        print(reward)
        #action = model.predict(observation)[0]