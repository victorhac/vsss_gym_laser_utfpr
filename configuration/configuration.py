import json
import os

def _get_configuration_dictionary(): 
    launch_data = _get_launch_data()
    mode = launch_data["mode"]
    return _get_configuration_dictionary_by_mode(mode)

def _get_launch_data():
    launch_file_path = os.path.join(
        os.path.dirname(__file__),
        "launch.json")
    
    return _get_data_from_json_file(launch_file_path)

def _get_configuration_dictionary_by_mode(mode: str):
    configuration_file_path = os.path.join(
        os.path.dirname(__file__),
        f"configuration.json")
    
    data = _get_data_from_json_file(configuration_file_path)

    configuration_file_path = os.path.join(
        os.path.dirname(__file__),
        f"configuration.{mode}.json")
    
    specific_data = _get_data_from_json_file(configuration_file_path)

    _merge_dicts(data, specific_data)

    return data

def _get_data_from_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.loads(f.read())
    return data

def _merge_dicts(base: dict, override: dict):
    for key, value in override.items():
        if isinstance(value, dict) and key in base and isinstance(base[key], dict):
            _merge_dicts(base[key], value)
        else:
            base[key] = value

class Configuration:
    configuration = _get_configuration_dictionary()
    motion_pid_constants_kp = configuration["motion"]["pid"]["constants"]["kp"]
    motion_pid_constants_ki = configuration["motion"]["pid"]["constants"]["ki"]
    motion_pid_constants_kd = configuration["motion"]["pid"]["constants"]["kd"]

    rsoccer_robot_wheel_radius = configuration["rsoccer"]["robot"]["wheel"]["radius"]
    rsoccer_robot_motor_max_rpm = configuration["rsoccer"]["robot"]["motor"]["max-rpm"]
    rsoccer_robot_speed_max_radians_seconds = configuration["rsoccer"]["robot"]["speed"]["max-radians-seconds"]
    rsoccer_robot_speed_dead_zone_meters_seconds = configuration["rsoccer"]["robot"]["speed"]["dead-zone-meters-seconds"]
    rsoccer_robot_width = configuration["rsoccer"]["robot"]["width"]
    rsoccer_robot_length = configuration["rsoccer"]["robot"]["length"]

    rsoccer_team_is_yellow_left_team = configuration["rsoccer"]["team"]["is-yellow-left-team"]
    rsoccer_team_is_yellow_team = configuration["rsoccer"]["team"]["is-yellow-team"]
    rsoccer_team_blue_number_robots = configuration["rsoccer"]["team"]["blue"]["number-robots"]
    rsoccer_team_yellow_number_robots = configuration["rsoccer"]["team"]["yellow"]["number-robots"]

    rsoccer_training_time_step = configuration["rsoccer"]["training"]["time-step"]
    rsoccer_training_episode_duration = configuration["rsoccer"]["training"]["episode-duration"]
    rsoccer_training_max_v = configuration["rsoccer"]["training"]["max-v"]
    rsoccer_training_max_distance = configuration["rsoccer"]["training"]["max-distance"]
    rsoccer_training_max_x = configuration["rsoccer"]["training"]["max-x"]
    rsoccer_training_max_y = configuration["rsoccer"]["training"]["max-y"]

    firasim_control_ip = configuration["firasim"]["control"]["ip"]
    firasim_control_port = configuration["firasim"]["control"]["port"]

    firasim_vision_ip = configuration["firasim"]["vision"]["ip"]
    firasim_vision_port = configuration["firasim"]["vision"]["port"]
    firasim_vision_buffer_size = configuration["firasim"]["vision"]["buffer"]["size"]

    firasim_robot_wheel_radius = configuration["firasim"]["robot"]["wheel"]["radius"]
    firasim_robot_speed_max_radians_seconds = configuration["firasim"]["robot"]["speed"]["max-radians-seconds"]
    firasim_robot_width = configuration["firasim"]["robot"]["width"]
    firasim_robot_length = configuration["firasim"]["robot"]["length"]

    firasim_team_is_yellow_left_team = configuration["firasim"]["team"]["is-yellow-left-team"]
    firasim_team_is_yellow_team = configuration["firasim"]["team"]["is-yellow-team"]
    firasim_team_blue_number_robots = configuration["firasim"]["team"]["blue"]["number-robots"]
    firasim_team_yellow_number_robots = configuration["firasim"]["team"]["yellow"]["number-robots"]

    referee_ip = configuration["referee"]["ip"]
    referee_port = configuration["referee"]["port"]
    referee_buffer_size = configuration["referee"]["buffer"]["size"]

    replacer_ip = configuration["replacer"]["ip"]
    replacer_port = configuration["replacer"]["port"]

    field_length = configuration["field"]["length"]
    field_width = configuration["field"]["width"]
    field_goal_width = configuration["field"]["goal"]["width"]
    field_goal_depth = configuration["field"]["goal"]["depth"]
    field_goal_area_length = configuration["field"]["goal-area"]["length"]
    field_goal_area_width = configuration["field"]["goal-area"]["width"]
    field_ball_radius = configuration["field"]["ball"]["radius"]

    model_attacker_path = configuration["model"]["attacker"]["path"]

    game_states_free_kick_team_positionings = configuration["game"]["states"]["free-kick"]["team"]["positionings"]
    game_states_free_kick_team_positionings_ball_x = game_states_free_kick_team_positionings["ball"]["x"]
    game_states_free_kick_team_positionings_ball_y = game_states_free_kick_team_positionings["ball"]["y"]
    game_states_free_kick_team_positionings_0_x = game_states_free_kick_team_positionings["0"]["x"]
    game_states_free_kick_team_positionings_0_y = game_states_free_kick_team_positionings["0"]["y"]
    game_states_free_kick_team_positionings_1_x = game_states_free_kick_team_positionings["1"]["x"]
    game_states_free_kick_team_positionings_1_y = game_states_free_kick_team_positionings["1"]["y"]
    game_states_free_kick_team_positionings_2_x = game_states_free_kick_team_positionings["2"]["x"]
    game_states_free_kick_team_positionings_2_y = game_states_free_kick_team_positionings["2"]["y"]

    game_states_free_kick_foe_team_positionings = configuration["game"]["states"]["free-kick"]["foe-team"]["positionings"]
    game_states_free_kick_foe_team_positionings_ball_x = game_states_free_kick_foe_team_positionings["ball"]["x"]
    game_states_free_kick_foe_team_positionings_ball_y = game_states_free_kick_foe_team_positionings["ball"]["y"]
    game_states_free_kick_foe_team_positionings_0_x = game_states_free_kick_foe_team_positionings["0"]["x"]
    game_states_free_kick_foe_team_positionings_0_y = game_states_free_kick_foe_team_positionings["0"]["y"]
    game_states_free_kick_foe_team_positionings_1_x = game_states_free_kick_foe_team_positionings["1"]["x"]
    game_states_free_kick_foe_team_positionings_1_y = game_states_free_kick_foe_team_positionings["1"]["y"]
    game_states_free_kick_foe_team_positionings_2_x = game_states_free_kick_foe_team_positionings["2"]["x"]
    game_states_free_kick_foe_team_positionings_2_y = game_states_free_kick_foe_team_positionings["2"]["y"]

    game_states_penalty_kick_team_positionings = configuration["game"]["states"]["penalty-kick"]["team"]["positionings"]
    game_states_penalty_kick_team_positionings_ball_x = game_states_penalty_kick_team_positionings["ball"]["x"]
    game_states_penalty_kick_team_positionings_ball_y = game_states_penalty_kick_team_positionings["ball"]["y"]
    game_states_penalty_kick_team_positionings_0_x = game_states_penalty_kick_team_positionings["0"]["x"]
    game_states_penalty_kick_team_positionings_0_y = game_states_penalty_kick_team_positionings["0"]["y"]
    game_states_penalty_kick_team_positionings_1_x = game_states_penalty_kick_team_positionings["1"]["x"]
    game_states_penalty_kick_team_positionings_1_y = game_states_penalty_kick_team_positionings["1"]["y"]
    game_states_penalty_kick_team_positionings_2_x = game_states_penalty_kick_team_positionings["2"]["x"]
    game_states_penalty_kick_team_positionings_2_y = game_states_penalty_kick_team_positionings["2"]["y"]

    game_states_penalty_kick_foe_team_positionings = configuration["game"]["states"]["penalty-kick"]["foe-team"]["positionings"]
    game_states_penalty_kick_foe_team_positionings_ball_x = game_states_penalty_kick_foe_team_positionings["ball"]["x"]
    game_states_penalty_kick_foe_team_positionings_ball_y = game_states_penalty_kick_foe_team_positionings["ball"]["y"]
    game_states_penalty_kick_foe_team_positionings_0_x = game_states_penalty_kick_foe_team_positionings["0"]["x"]
    game_states_penalty_kick_foe_team_positionings_0_y = game_states_penalty_kick_foe_team_positionings["0"]["y"]
    game_states_penalty_kick_foe_team_positionings_1_x = game_states_penalty_kick_foe_team_positionings["1"]["x"]
    game_states_penalty_kick_foe_team_positionings_1_y = game_states_penalty_kick_foe_team_positionings["1"]["y"]
    game_states_penalty_kick_foe_team_positionings_2_x = game_states_penalty_kick_foe_team_positionings["2"]["x"]
    game_states_penalty_kick_foe_team_positionings_2_y = game_states_penalty_kick_foe_team_positionings["2"]["y"]

    game_states_goal_kick_team_positionings = configuration["game"]["states"]["goal-kick"]["team"]["positionings"]
    game_states_goal_kick_team_positionings_ball_x = game_states_goal_kick_team_positionings["ball"]["x"]
    game_states_goal_kick_team_positionings_ball_y = game_states_goal_kick_team_positionings["ball"]["y"]
    game_states_goal_kick_team_positionings_0_x = game_states_goal_kick_team_positionings["0"]["x"]
    game_states_goal_kick_team_positionings_0_y = game_states_goal_kick_team_positionings["0"]["y"]
    game_states_goal_kick_team_positionings_1_x = game_states_goal_kick_team_positionings["1"]["x"]
    game_states_goal_kick_team_positionings_1_y = game_states_goal_kick_team_positionings["1"]["y"]
    game_states_goal_kick_team_positionings_2_x = game_states_goal_kick_team_positionings["2"]["x"]
    game_states_goal_kick_team_positionings_2_y = game_states_goal_kick_team_positionings["2"]["y"]

    game_states_free_ball_quadrant_1_positionings = configuration["game"]["states"]["free-ball"]["quadrant-1"]["positionings"]
    game_states_free_ball_quadrant_1_positionings_ball_x = game_states_free_ball_quadrant_1_positionings["ball"]["x"]
    game_states_free_ball_quadrant_1_positionings_ball_y = game_states_free_ball_quadrant_1_positionings["ball"]["y"]
    game_states_free_ball_quadrant_1_positionings_0_main_x = game_states_free_ball_quadrant_1_positionings["0"]["main"]["x"]
    game_states_free_ball_quadrant_1_positionings_0_main_y = game_states_free_ball_quadrant_1_positionings["0"]["main"]["y"]
    game_states_free_ball_quadrant_1_positionings_0_secondary_x = game_states_free_ball_quadrant_1_positionings["0"]["secondary"]["x"]
    game_states_free_ball_quadrant_1_positionings_0_secondary_y = game_states_free_ball_quadrant_1_positionings["0"]["secondary"]["y"]
    game_states_free_ball_quadrant_1_positionings_1_x = game_states_free_ball_quadrant_1_positionings["1"]["x"]
    game_states_free_ball_quadrant_1_positionings_1_y = game_states_free_ball_quadrant_1_positionings["1"]["y"]
    game_states_free_ball_quadrant_1_positionings_2_x = game_states_free_ball_quadrant_1_positionings["2"]["x"]
    game_states_free_ball_quadrant_1_positionings_2_y = game_states_free_ball_quadrant_1_positionings["2"]["y"]

    game_states_free_ball_quadrant_2_positionings = configuration["game"]["states"]["free-ball"]["quadrant-2"]["positionings"]
    game_states_free_ball_quadrant_2_positionings_ball_x = game_states_free_ball_quadrant_2_positionings["ball"]["x"]
    game_states_free_ball_quadrant_2_positionings_ball_y = game_states_free_ball_quadrant_2_positionings["ball"]["y"]
    game_states_free_ball_quadrant_2_positionings_0_main_x = game_states_free_ball_quadrant_2_positionings["0"]["main"]["x"]
    game_states_free_ball_quadrant_2_positionings_0_main_y = game_states_free_ball_quadrant_2_positionings["0"]["main"]["y"]
    game_states_free_ball_quadrant_2_positionings_0_secondary_x = game_states_free_ball_quadrant_2_positionings["0"]["secondary"]["x"]
    game_states_free_ball_quadrant_2_positionings_0_secondary_y = game_states_free_ball_quadrant_2_positionings["0"]["secondary"]["y"]
    game_states_free_ball_quadrant_2_positionings_1_x = game_states_free_ball_quadrant_2_positionings["1"]["x"]
    game_states_free_ball_quadrant_2_positionings_1_y = game_states_free_ball_quadrant_2_positionings["1"]["y"]
    game_states_free_ball_quadrant_2_positionings_2_x = game_states_free_ball_quadrant_2_positionings["2"]["x"]
    game_states_free_ball_quadrant_2_positionings_2_y = game_states_free_ball_quadrant_2_positionings["2"]["y"]

    game_states_free_ball_quadrant_3_positionings = configuration["game"]["states"]["free-ball"]["quadrant-3"]["positionings"]
    game_states_free_ball_quadrant_3_positionings_ball_x = game_states_free_ball_quadrant_3_positionings["ball"]["x"]
    game_states_free_ball_quadrant_3_positionings_ball_y = game_states_free_ball_quadrant_3_positionings["ball"]["y"]
    game_states_free_ball_quadrant_3_positionings_0_main_x = game_states_free_ball_quadrant_3_positionings["0"]["main"]["x"]
    game_states_free_ball_quadrant_3_positionings_0_main_y = game_states_free_ball_quadrant_3_positionings["0"]["main"]["y"]
    game_states_free_ball_quadrant_3_positionings_0_secondary_x = game_states_free_ball_quadrant_3_positionings["0"]["secondary"]["x"]
    game_states_free_ball_quadrant_3_positionings_0_secondary_y = game_states_free_ball_quadrant_3_positionings["0"]["secondary"]["y"]
    game_states_free_ball_quadrant_3_positionings_1_x = game_states_free_ball_quadrant_3_positionings["1"]["x"]
    game_states_free_ball_quadrant_3_positionings_1_y = game_states_free_ball_quadrant_3_positionings["1"]["y"]
    game_states_free_ball_quadrant_3_positionings_2_x = game_states_free_ball_quadrant_3_positionings["2"]["x"]
    game_states_free_ball_quadrant_3_positionings_2_y = game_states_free_ball_quadrant_3_positionings["2"]["y"]

    game_states_free_ball_quadrant_4_positionings = configuration["game"]["states"]["free-ball"]["quadrant-4"]["positionings"]
    game_states_free_ball_quadrant_4_positionings_ball_x = game_states_free_ball_quadrant_4_positionings["ball"]["x"]
    game_states_free_ball_quadrant_4_positionings_ball_y = game_states_free_ball_quadrant_4_positionings["ball"]["y"]
    game_states_free_ball_quadrant_4_positionings_0_main_x = game_states_free_ball_quadrant_4_positionings["0"]["main"]["x"]
    game_states_free_ball_quadrant_4_positionings_0_main_y = game_states_free_ball_quadrant_4_positionings["0"]["main"]["y"]
    game_states_free_ball_quadrant_4_positionings_0_secondary_x = game_states_free_ball_quadrant_4_positionings["0"]["secondary"]["x"]
    game_states_free_ball_quadrant_4_positionings_0_secondary_y = game_states_free_ball_quadrant_4_positionings["0"]["secondary"]["y"]
    game_states_free_ball_quadrant_4_positionings_1_x = game_states_free_ball_quadrant_4_positionings["1"]["x"]
    game_states_free_ball_quadrant_4_positionings_1_y = game_states_free_ball_quadrant_4_positionings["1"]["y"]
    game_states_free_ball_quadrant_4_positionings_2_x = game_states_free_ball_quadrant_4_positionings["2"]["x"]
    game_states_free_ball_quadrant_4_positionings_2_y = game_states_free_ball_quadrant_4_positionings["2"]["y"]

    game_states_kickoff_team_team_positionings = configuration["game"]["states"]["kickoff"]["team"]["positionings"]
    game_states_kickoff_team_positionings_ball_x = game_states_kickoff_team_team_positionings["ball"]["x"]
    game_states_kickoff_team_positionings_ball_y = game_states_kickoff_team_team_positionings["ball"]["y"]
    game_states_kickoff_team_positionings_0_x = game_states_kickoff_team_team_positionings["0"]["x"]
    game_states_kickoff_team_positionings_0_y = game_states_kickoff_team_team_positionings["0"]["y"]
    game_states_kickoff_team_positionings_1_x = game_states_kickoff_team_team_positionings["1"]["x"]
    game_states_kickoff_team_positionings_1_y = game_states_kickoff_team_team_positionings["1"]["y"]
    game_states_kickoff_team_positionings_2_x = game_states_kickoff_team_team_positionings["2"]["x"]
    game_states_kickoff_team_positionings_2_y = game_states_kickoff_team_team_positionings["2"]["y"]

    game_states_kickoff_team_foe_team_positionings = configuration["game"]["states"]["kickoff"]["foe-team"]["positionings"]
    game_states_kickoff_foe_team_positionings_ball_x = game_states_kickoff_team_foe_team_positionings["ball"]["x"]
    game_states_kickoff_foe_team_positionings_ball_y = game_states_kickoff_team_foe_team_positionings["ball"]["y"]
    game_states_kickoff_foe_team_positionings_0_x = game_states_kickoff_team_foe_team_positionings["0"]["x"]
    game_states_kickoff_foe_team_positionings_0_y = game_states_kickoff_team_foe_team_positionings["0"]["y"]
    game_states_kickoff_foe_team_positionings_1_x = game_states_kickoff_team_foe_team_positionings["1"]["x"]
    game_states_kickoff_foe_team_positionings_1_y = game_states_kickoff_team_foe_team_positionings["1"]["y"]
    game_states_kickoff_foe_team_positionings_2_x = game_states_kickoff_team_foe_team_positionings["2"]["x"]
    game_states_kickoff_foe_team_positionings_2_y = game_states_kickoff_team_foe_team_positionings["2"]["y"]

    def get_firasim_is_left_team():
        return Configuration.firasim_team_is_yellow_left_team \
            == Configuration.firasim_team_is_yellow_team