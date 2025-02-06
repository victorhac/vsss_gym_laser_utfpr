import json
import numpy as np
from lib.builders.robot_curriculum_behavior_builder import RobotCurriculumBehaviorBuilder
from lib.domain.ball_curriculum_behavior import BallCurriculumBehavior
from lib.domain.curriculum_task import CurriculumTask
from lib.domain.enums.robot_curriculum_behavior_enum import RobotCurriculumBehaviorEnum
from lib.environment.attacker_environment import AttackerEnvironment
from lib.environment.defender_environment import DefenderEnvironment
from lib.position_setup.behind_ball_position_setup import BehindBallPositionSetup
from lib.position_setup.fixed_position_setup import FixedPositionSetup
from lib.utils.model_utils import ModelUtils, _load_ppo_model
from lib.utils.roles.attacker.attacker_v2_utils import AttackerV2Utils
from lib.utils.roles.attacker_utils import AttackerUtils
from lib.utils.roles.defender_utils import DefenderUtils

robot_position = FixedPositionSetup((0, 0))
defender_position = BehindBallPositionSetup(False)
defender_position.theta = 180
ball_position = FixedPositionSetup((0, 0))

def get_behavior():
    builder = RobotCurriculumBehaviorBuilder(
        0,
        False,
        100,
        robot_position
    )

    return builder\
        .set_from_model_behavior()\
        .build()

def get_attacker_behavior():
    builder = RobotCurriculumBehaviorBuilder(
        0,
        True,
        100,
        defender_position
    )

    builder.robot_curriculum_behavior_enum = RobotCurriculumBehaviorEnum.BALL_FOLLOWING

    return builder\
        .set_distance_range((0.15, 0.15))\
        .build()

def get_ball_behavior():
    return BallCurriculumBehavior(
        100,
        ball_position
    )

render = "human"

positions = []

min_x = -0.65
min_y = -0.55
max_x = -0.1
max_y = 0.55

for x in np.arange(min_x, max_x, (max_x - min_x) / 10):
    for y in np.arange(min_y, max_y, (max_y - min_y) / 5):
        positions.append((x, y))
        positions.append((max_x - x , y))

behaviors = [get_behavior(), get_attacker_behavior()]
ball_behavior = get_ball_behavior()

task = CurriculumTask(
    "",
    behaviors,
    ball_behavior,
    update_count=0,
    updates_per_task=100,
    games_count=100,
    default_threshold=.98)

env = DefenderEnvironment(task, render)

model = ModelUtils.defender_model()

mean_rewards = []
gols_feitos = 0
gols_sofridos = 0

for position in positions:
    reward = 0
    accumulated_reward = 0
    steps = 0

    done = False
    robot_position.position = position[0]
    ball_position.position = position[1]
    obs = env.reset()

    while not done:
        observation = DefenderUtils.get_observation(env, 0, False, True)
        action = model.predict(observation, deterministic=True)[0]

        next_state, reward, done, _, _ = env.step(action)
        env.render()
        steps += 1
        accumulated_reward += reward

    if env._any_team_scored_goal():
        if env._has_scored_goal():
            gols_feitos += 1
        else:
            gols_sofridos += 1

    mean_rewards.append(accumulated_reward / steps)

# result = {
#     "mean_rewards": mean_rewards,
#     "gols_feitos": gols_feitos,
#     "gols_sofridos": gols_sofridos
# }

# with open("./evaluation/attacker_evaluation.json", "w") as f:
#     json.dump(result, f)