from lib.environment.team.team_v2_environment import TeamV2Environment
from lib.utils.behavior.team.team_v2_behavior_utils import TeamV2BehaviorUtils
from lib.utils.model_utils import ModelUtils
from lib.utils.roles.team_utils import TeamUtils

render_mode = 'human'

update_count = 2
updates_per_task = 2
games_count = 2
default_threshold = 0.5

model = ModelUtils.team_model()

task = TeamV2BehaviorUtils.get_task_1(
    update_count,
    updates_per_task,
    games_count,
    default_threshold
)

env = TeamV2Environment(task, render_mode)

while True:
    obs = env.reset()
    reward = 0
    done = False
    action = (0, 0, 0)

    while not done:
        next_state, reward, done, _, _ = env.step(action)
        print(reward)
        env.render()
        observation = TeamUtils.get_observation(env, False, True)
        action = model.predict(observation)[0]