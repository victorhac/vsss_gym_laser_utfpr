from configuration.configuration import Configuration
from lib.domain.enums.foul_enum import FoulEnum
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

number_of_matches = 100
match_time = 60
time_step = Configuration.rsoccer_training_time_step
foe_team_name = "two_attackers_one_goalkeeper_with_blocked_goalkeeper"
debug = False

if debug:
    render_mode = "human"
    do_log = False
else:
    render_mode = "rgb_array"
    do_log = True

attacker_model = ModelUtils.attacker_model()
defender_model = ModelUtils.defender_model()
goalkeeper_model = ModelUtils.goalkeeper_model()
team_model = ModelUtils.team_model()

env = EvaluationEnvironment(render_mode)

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
        attacker_model,
        False
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
        defender_model,
        False
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
        goalkeeper_model,
        False
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

    return right_speed / 30, left_speed / 30

def get_team_actions(
    is_yellow: bool,
    is_left_team: bool
):
    return TeamUtils.get_action(
        env,
        team_model,
        is_yellow,
        is_left_team,
        False
    )

def get_team_behavior():
    action = []
    team_action = get_team_actions(False, True)

    for i in range(3):
        if i == 2:
            action.extend(get_goalkeeper_action(i, False, True))
        elif team_action[i] == 0:
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
    action.extend(get_attacker_action(1, True, False))
    action.extend(get_goalkeeper_action(2, True, False))
    return action

def get_action():
    action = []
    action.extend(get_team_behavior())
    action.extend(get_foe_behavior())
    return action

def log(text: str):
    with open(f"evaluation/{foe_team_name}.txt", 'a') as file:
        file.write(text)

number_of_wins = 0
number_of_draws = 0
number_of_losses = 0
total_number_of_goals_pro = 0
total_number_of_goals_against = 0
total_number_of_offensive_free_balls = 0
total_number_of_defensive_free_balls = 0
total_defensive_field_percentage = 0
total_offensive_field_percentage = 0

matches_count = 0

while matches_count < number_of_matches:
    step_count = 0
    goals_pro = 0
    goals_against = 0
    offensive_free_ball_count = 0
    defensive_free_ball_count = 0
    offensive_field_step_count = 0
    defensive_field_step_count = 0

    _ = env.reset()

    reward = 0
    done = False
    action = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    while step_count * time_step < match_time:
        next_state, reward, done, _, _ = env.step(action)
        env.render()
        step_count += 1
        action = get_action()

        if env._get_ball().x < 0:
            defensive_field_step_count += 1
        else:
            offensive_field_step_count += 1

        if env.is_ball_stucked():
            env.foul_enum = FoulEnum.FREE_BALL

            if env._get_ball().x < 0:
                defensive_free_ball_count += 1
            else:
                offensive_free_ball_count += 1

            env.reset()

        elif env._any_team_scored_goal():
            if env._has_scored_goal():
                goals_pro += 1
            elif env._has_received_goal():
                goals_against += 1
    
            env.foul_enum = FoulEnum.KICKOFF
            env.reset()

    defensive_field_percentage = defensive_field_step_count / step_count
    offensive_field_percentage = offensive_field_step_count / step_count

    total_number_of_goals_pro += goals_pro
    total_number_of_goals_against += goals_against
    total_number_of_offensive_free_balls += offensive_free_ball_count
    total_number_of_defensive_free_balls += defensive_free_ball_count
    total_defensive_field_percentage += defensive_field_percentage
    total_offensive_field_percentage += offensive_field_percentage

    if goals_pro > goals_against:
        number_of_wins += 1
    elif goals_pro == goals_against:
        number_of_draws += 1
    else:
        number_of_losses += 1

    if do_log:
        log(f"Match {matches_count + 1}; Goals pro: {goals_pro}; Goals against: {goals_against}; Offensive Free balls: {offensive_free_ball_count}; Defensive Free balls: {defensive_free_ball_count}; Offensive field percentage: {offensive_field_percentage}; Defensive field percentage: {defensive_field_percentage}\n")

    matches_count += 1

if do_log:
    log(f"Number of wins: {number_of_wins}; Number of draws: {number_of_draws}; Number of losses: {number_of_losses}; Total number of goals pro: {total_number_of_goals_pro}; Total number of goals against: {total_number_of_goals_against}; Total number of offensive free balls: {total_number_of_offensive_free_balls}; Total number of defensive free balls: {total_number_of_defensive_free_balls}; Mean defensive field percentage: {total_defensive_field_percentage / number_of_matches}; Mean offensive field percentage: {total_offensive_field_percentage / number_of_matches}\n")