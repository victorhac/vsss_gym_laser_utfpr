from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.monitor import Monitor

from lib.curriculum.behavior_callback import BehaviorCallback
from lib.environment.team_environment import TeamEnvironment
from lib.utils.behavior.team_behavior_utils import TeamBehaviorUtils

import os
from datetime import datetime

task_training_name = "team"
algorithm_name = "PPO"

render_mode = "rgb_array"

num_threads = 14

total_timesteps = 400_000_000

gae_lambda = 0.95
gamma = 0.99
learning_rate = 0.0004
clip_range = 0.2
policy = "MlpPolicy"
batch_size = 128

device = "cpu"

load_model = False
loaded_model_path = ""

check_count = 100
starting_update = 0

log_interval = total_timesteps // 10

def create_env(
    save_path,
    index,
    first_task_function
):
    def _init():
        env = TeamEnvironment(first_task_function(), render_mode)
        return Monitor(env, f"{save_path}/monitor_log/env_{index}")
    return _init

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def get_datetime_folder_name():
    current_datetime = datetime.now()

    year = current_datetime.year
    month = current_datetime.month
    day = current_datetime.day
    hour = current_datetime.hour
    minute = current_datetime.minute
    second = current_datetime.second

    return f"{year}_{month}_{day}_{hour}_{minute}_{second}"

def get_task_models_path():
    return f"models/{task_training_name}/{algorithm_name}/{get_datetime_folder_name()}"

def main():
    get_first_task = lambda: TeamBehaviorUtils.get_task_1(starting_update)

    tasks = [
        get_first_task(),
        TeamBehaviorUtils.get_task_1(),
        TeamBehaviorUtils.get_task_2(),
        TeamBehaviorUtils.get_task_3(),
        TeamBehaviorUtils.get_task_4()
    ]

    save_path = get_task_models_path()

    create_folder_if_not_exists(save_path)

    env = SubprocVecEnv([
        create_env(
            save_path,
            i,
            get_first_task
        )
        for i in range(num_threads)
    ])

    model = PPO(
        policy=policy,
        env=env,
        gamma=gamma,
        learning_rate=learning_rate,
        gae_lambda=gae_lambda,
        clip_range=clip_range,
        batch_size=batch_size,
        device=device)

    if load_model:
        model.set_parameters(loaded_model_path)

    checkpoint_callback = BehaviorCallback(
        check_count=check_count,
        total_timesteps=total_timesteps,
        model_name=algorithm_name,
        save_path=save_path,
        log_path=save_path,
        tasks=tasks)
    
    try:
        model.learn(
            total_timesteps=total_timesteps,
            log_interval=log_interval,
            callback=checkpoint_callback,
            progress_bar=True)
    except:
        if int(input("Save current model: 1 - Yes, 2 - No")) == 1:
            model.save(f"{save_path}/interrupted_model")
    
if __name__ == '__main__':
    main()