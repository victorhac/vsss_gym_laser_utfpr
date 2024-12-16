from lib.environment.defender_environment import DefenderEnvironment
import matplotlib.pyplot as plt

from lib.utils.behavior.defender_behavior_utils import DefenderBehaviorUtils
from lib.utils.environment.attacker_environment_utils import AttackerEnvironmentUtils

from configuration.configuration import Configuration
from lib.utils.file_utils import FileUtils

render_mode = "human"
plot_file = "temp/plot.png"

tasks = [
    DefenderBehaviorUtils.get_task_1,
    DefenderBehaviorUtils.get_task_2,
    DefenderBehaviorUtils.get_task_3,
    DefenderBehaviorUtils.get_task_4,
    DefenderBehaviorUtils.get_task_5
]

FileUtils.remove_file_if_exists(plot_file)

def load_model():
    from stable_baselines3 import PPO
    return PPO.load(Configuration.get_model_attacker_path())

def plot_reward(reward_per_step: list):
    plt.plot(reward_per_step)
    plt.xlabel("Step")
    plt.ylabel("Reward")
    plt.title("Step Rewards over Time")
    plt.legend()
    plt.grid()
    plt.savefig(plot_file)

def get_task(
    index: int,
    update_count: int,
    updates_per_task: int,
    games_count: int,
    default_threshold: float
):
    return tasks[index](
        update_count,
        updates_per_task,
        games_count,
        default_threshold
    )

is_left_team = True
is_yellow = False
robot_id = 0

update_count = 3
updates_per_task = 3
games_count = 100
default_threshold = .8

task_index = 4

task = get_task(
    task_index,
    update_count,
    updates_per_task,
    games_count,
    default_threshold)

env = DefenderEnvironment(task, render_mode)

model = load_model()

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
        action, _ = model.predict(
            AttackerEnvironmentUtils.get_observation(
                env,
                robot_id,
                is_yellow,
                is_left_team
            ))

    plot_reward(reward_per_step)

    input("Continue...")

    reward_per_step.clear()