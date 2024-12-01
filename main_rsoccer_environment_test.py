from stable_baselines3 import PPO
from lib.utils.behavior.attacker_behavior_utils import AttackerBehaviorUtils
from lib.environment.defender.environment import Environment
import matplotlib.pyplot as plt

render_mode = "human"

def plot_reward(reward_per_step: list):
    plt.plot(reward_per_step)
    plt.xlabel("Step")
    plt.ylabel("Reward")
    plt.title("Step Rewards over Time")
    plt.legend()
    plt.grid()
    plt.savefig('temp/plot.png')

task = AttackerBehaviorUtils.get_task_1(97)

env = Environment(task, render_mode)

model = PPO.load("models/attacker/PPO/2024_9_24_14_48_13/PPO_model_task_6_update_117_13999986_steps.zip")

env.opponent_model = model

reward_per_step = []

while True:
    obs = env.reset()
    reward = 0
    done = False
    action = (0, 0)

    while not done:
        next_state, reward, done, _, _ = env.step((action[0] / 2, action[1] / 2))
        env.render()

        reward_per_step.append(reward)
        action, _ = model.predict(next_state)

    plot_reward(reward_per_step)

    input("Continue....")

    reward_per_step.clear()