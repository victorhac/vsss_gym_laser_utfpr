from lib.domain.field import Field
from lib.environment.evaluation.evaluation_environment import EvaluationEnvironment
from lib.positioning.default_supporter_positioning import get_supporter_position
from lib.utils.field_utils import FieldUtils
from lib.utils.model_utils import ModelUtils
from lib.utils.motion_utils import MotionUtils
from lib.utils.roles.attacker_utils import AttackerUtils
from lib.utils.roles.defender_utils import DefenderUtils
from lib.utils.roles.goalkeeper_utils import GoalkeeperUtils
from lib.utils.roles.team_utils import TeamUtils
from lib.utils.rsoccer.rsoccer_utils import RSoccerUtils

attacker_model = ModelUtils.attacker_model()
defender_model = ModelUtils.defender_model()
goalkeeper_model = ModelUtils.goalkeeper_model()
team_model = ModelUtils.team_model()

env = EvaluationEnvironment("human")

def get_attacker_action(
    robot_id: int,
    is_yellow: bool,
    is_left_team: bool
):
    return AttackerUtils.get_action(
        env,
        robot_id,
        is_yellow,
        is_left_team,
        attacker_model
    )

def get_defender_action(
    robot_id: int,
    is_yellow: bool,
    is_left_team: bool
):
    return DefenderUtils.get_action(
        env,
        robot_id,
        is_yellow,
        is_left_team,
        defender_model
    )

def get_goalkeeper_action(
    robot_id: int,
    is_yellow: bool,
    is_left_team: bool
):
    return GoalkeeperUtils.get_action(
        env,
        robot_id,
        is_yellow,
        is_left_team,
        goalkeeper_model
    )

def get_supporter_action(
    robot_id: int,
    is_left_team: bool
):
    field = RSoccerUtils.get_field_by_frame(env.frame, not is_left_team)
    robot = field.get_robot_by_id(robot_id)
    position = get_supporter_position(robot_id, field)
    obstacles = FieldUtils.to_obstacles_except_current_robot_and_ball(
        field,
        robot_id
    )

    left_speed, right_speed = MotionUtils.go_to_point_univector(
        robot,
        position,
        obstacles
    )

    return left_speed / 30, right_speed / 30

def get_team_actions(
    is_yellow: bool,
    is_left_team: bool
):
    return TeamUtils.get_action(
        env,
        team_model,
        is_yellow,
        is_left_team
    )

def get_team_behavior():
    action = []
    team_action = get_team_actions(False, True)

    for i in range(3):
        if team_action[i] == 0:
            action.extend(get_attacker_action(i, False, True))
        elif team_action[i] == 1:
            action.extend(get_defender_action(i, False, True))
        elif team_action[i] == 2:
            action.extend(get_goalkeeper_action(i, False, True))
        elif team_action[i] == 3:
            action.extend(get_supporter_action(i, True))

    return action

def get_foe_behavior():
    action = []
    action.extend(get_attacker_action(0, True, False))
    action.extend(get_defender_action(1, True, False))
    action.extend(get_goalkeeper_action(2, True, False))
    return action

def get_action():
    action = []
    action.extend(get_team_behavior())
    action.extend(get_foe_behavior())
    return action

while True:
    _ = env.reset()
    reward = 0
    done = False
    action = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    while not done:
        next_state, reward, done, _, _ = env.step(action)
        env.render()
        action = get_action()