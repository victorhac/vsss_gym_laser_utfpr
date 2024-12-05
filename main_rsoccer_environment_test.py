from stable_baselines3 import PPO
from lib.environment.defender_environment import DefenderEnvironment
import matplotlib.pyplot as plt

from lib.utils.behavior.defender_behavior_utils import DefenderBehaviorUtils
from lib.utils.environment.attacker_environment_utils import AttackerEnvironmentUtils

render_mode = "human"

def plot_reward(reward_per_step: list):
    plt.plot(reward_per_step)
    plt.xlabel("Step")
    plt.ylabel("Reward")
    plt.title("Step Rewards over Time")
    plt.legend()
    plt.grid()
    plt.savefig('temp/plot.png')

task = DefenderBehaviorUtils.get_task_1(1)

env = DefenderEnvironment(task, render_mode)

model = PPO.load("models/attacker/PPO/2024_9_24_14_48_13/PPO_model_task_6_update_117_13999986_steps.zip")

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
        action, _ = model.predict(AttackerEnvironmentUtils.get_observation(env, env.robot_id, False, False))

    plot_reward(reward_per_step)

    input("Continue....")

    reward_per_step.clear()