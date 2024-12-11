from stable_baselines3 import PPO
from lib.environment.defender_environment import DefenderEnvironment
import matplotlib.pyplot as plt

from lib.utils.behavior.defender_behavior_utils import DefenderBehaviorUtils
from lib.utils.environment.attacker_environment_utils import AttackerEnvironmentUtils

from configuration.configuration import Configuration

render_mode = "human"

def plot_reward(reward_per_step: list):
    plt.plot(reward_per_step)
    plt.xlabel("Step")
    plt.ylabel("Reward")
    plt.title("Step Rewards over Time")
    plt.legend()
    plt.grid()
    plt.savefig('temp/plot.png')

update_count = 0
updates_per_task = 3
games_count = 100
default_threshold = .8

task = DefenderBehaviorUtils.get_task_2(
    update_count,
    updates_per_task,
    games_count,
    default_threshold)

env = DefenderEnvironment(task, render_mode)

model = PPO.load(Configuration.get_model_attacker_path())

reward_per_step = []

while True:
    obs = env.reset()
    reward = 0
    done = False
    action = (0, 0)

    while not done:
        next_state, reward, done, _, _ = env.step(action)
        env.render()

        reward_per_step.append(reward)
        action, _ = model.predict(AttackerEnvironmentUtils.get_observation(env, env.robot_id, False, True))

    plot_reward(reward_per_step)

    input("Continue...")

    reward_per_step.clear()