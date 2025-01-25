from stable_baselines3 import PPO
from lib.environment.test_environment import TestEnvironment

from lib.path_planning.univector_field_navigation import get_univector_field_point_theta
from lib.positioning.default_supporter_positioning import get_supporter_position
from lib.utils.field_utils import FieldUtils
from lib.utils.motion_utils import MotionUtils
from lib.utils.roles.attacker_utils import AttackerUtils
from lib.utils.roles.defender_utils import DefenderUtils
from lib.utils.roles.goalkeeper_utils import GoalkeeperUtils
from lib.utils.rsoccer_utils import RSoccerUtils

render_mode = "human"

def load_model(model_path: str):
    from stable_baselines3 import PPO
    return PPO.load(model_path)

def load_attacker_model():
    return load_model("models/attacker/PPO/2024_9_24_14_48_13/PPO_model_task_6_update_117_13999986_steps.zip")

def load_defender_model():
    return load_model("models/defender/PPO/2025_1_3_23_6_42/interrupted_model.zip")

def load_goalkeeper_model():
    return load_model("models/goalkeeper/PPO/2025_1_4_18_57_50/PPO_model_task_1_update_100_102286296_steps.zip")

env = TestEnvironment(render_mode)

attacker_model = load_attacker_model()
defender_model = load_defender_model()
goalkeeper_model = load_goalkeeper_model()

def get_action(model: PPO, robot_id: int, is_yellow: bool, is_left: bool, get_observation_func):
    observation = get_observation_func(env, robot_id, is_yellow, is_left)
    action, _ = model.predict(observation)
    return action

def get_attacker_action(robot_id: int, is_yellow: bool, is_left: bool):
    return get_action(attacker_model, robot_id, is_yellow, is_left, AttackerUtils.get_observation)

def get_defender_action(robot_id: int, is_yellow: bool, is_left: bool):
    return get_action(defender_model, robot_id, is_yellow, is_left, DefenderUtils.get_observation)

def get_supporter_action(robot_id: int, is_yellow: bool, is_left: bool):
    field = RSoccerUtils.get_field_by_frame(
        env.frame,
        is_yellow
    )
    desired_position = get_supporter_position(
        robot_id,
        field
    )
    obstacles = FieldUtils.to_obstacles_except_current_robot_and_ball(
        field,
        robot_id
    )
    robot = field.robots[robot_id]
    theta = get_univector_field_point_theta(
        robot.get_position_tuple(),
        robot.get_velocity_tuple(),
        desired_position,
        obstacles
    )

    left_speed, right_speed = MotionUtils.go_to_point_by_theta(
        robot,
        theta)
    
    return right_speed / 30, left_speed / 30

def get_goalkeeper_action(robot_id: int, is_yellow: bool, is_left: bool):
    return get_action(goalkeeper_model, robot_id, is_yellow, is_left, GoalkeeperUtils.get_observation)

def get_actions():
    action = []

    action.extend(get_attacker_action(0, False, True))
    action.extend(get_supporter_action(1, False, True))
    action.extend(get_goalkeeper_action(2, False, True))

    action.extend(get_attacker_action(0, True, False))
    action.extend(get_defender_action(1, True, False))
    action.extend(get_goalkeeper_action(2, True, False))

    return action

reward_per_step = []

while True:
    obs = env.reset()
    reward = 0
    done = False
    action = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    while not done:
        next_state, reward, done, _, _ = env.step(action)
        env.render()

        reward_per_step.append(reward)
        action = get_actions()

    #input("Continue...")

    reward_per_step.clear()