from lib.environment.goalkeeper_environment import GoalkeeperEnvironment
import matplotlib.pyplot as plt

from lib.utils.behavior.goalkeeper_behavior_utils import GoalkeeperBehaviorUtils

from lib.utils.file_utils import FileUtils

render_mode = "human"
plot_file = "temp/plot.png"
should_load_model = True
model_path = "models/goalkeeper/PPO/2025_1_4_18_57_50/PPO_model_task_1_update_100_102286296_steps.zip"

is_left_team = True
is_yellow = False
robot_id = 0

update_count = 100
updates_per_task = 100
games_count = 100
default_threshold = .8

task_id = 1

tasks = [
    GoalkeeperBehaviorUtils.get_task_1
]

FileUtils.remove_file_if_exists(plot_file)

def load_model():
    from stable_baselines3 import PPO
    return PPO.load(model_path)

def plot_reward(reward_per_step: list):
    plt.plot(reward_per_step)
    plt.xlabel("Step")
    plt.ylabel("Reward")
    plt.title("Step Rewards over Time")
    plt.legend()
    plt.grid()
    plt.savefig(plot_file)

def get_task(id: int):
    return tasks[id - 1](
        update_count,
        updates_per_task,
        games_count,
        default_threshold
    )

task = get_task(task_id)

env = GoalkeeperEnvironment(task, render_mode)

model = load_model() if should_load_model else None

def get_action(next_state):
    if should_load_model:
        action, _ = model.predict(next_state)
        return action
    return 0, 0

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
        action = get_action(next_state)

    plot_reward(reward_per_step)

    #input("Continue...")

    reward_per_step.clear()