import json
import os

class Configuration:
    __configuration = None

    @staticmethod
    def _get_configuration():
        if Configuration.__configuration is not None:
            return Configuration.__configuration
        
        launch_data = Configuration.get_launch_data()

        mode = launch_data["mode"]
        
        configuration = Configuration.get_configuration_data(mode)

        Configuration.__configuration = configuration

        return configuration
    
    @staticmethod
    def get_launch_data():
        launch_file_path = os.path.join(
            os.path.dirname(__file__),
            "launch.json")
        
        return Configuration.get_data_from_json_file(launch_file_path)
    
    @staticmethod
    def get_configuration_data(mode: str):
        configuration_file_path = os.path.join(
            os.path.dirname(__file__),
            f"configuration.{mode}.json")
        
        return Configuration.get_data_from_json_file(configuration_file_path)
    
    @staticmethod
    def get_data_from_json_file(file_path):
        with open(file_path, 'r') as f:
            data = json.loads(f.read())
        return data
    
    @staticmethod
    def _get_rsoccer_configuration():
        configuration = Configuration._get_configuration()
        return configuration["rsoccer"]
    
    @staticmethod
    def _get_firasim_configuration():
        configuration = Configuration._get_configuration()
        return configuration["firasim"]
    
    @staticmethod
    def _get_motion_configuration():
        configuration = Configuration._get_configuration()
        return configuration["motion"]
    
    @staticmethod
    def get_motion_pid_constants():
        configuration = Configuration._get_motion_configuration()
        return configuration["pid"]["constants"]
    
    @staticmethod
    def get_motion_pid_constants_kp():
        configuration = Configuration.get_motion_pid_constants()
        return configuration["kp"]
    
    @staticmethod
    def get_motion_pid_constants_ki():
        configuration = Configuration.get_motion_pid_constants()
        return configuration["ki"]
    
    @staticmethod
    def get_motion_pid_constants_kd():
        configuration = Configuration.get_motion_pid_constants()
        return configuration["kd"]
    
    @staticmethod
    def get_rsoccer_robot_wheel_radius():
        configuration = Configuration._get_rsoccer_configuration()
        return configuration["robot"]["wheel"]["radius"]
    
    @staticmethod
    def get_rsoccer_robot_motor_max_rpm():
        configuration = Configuration._get_rsoccer_configuration()
        return configuration["robot"]["motor"]["max-rpm"]
    
    @staticmethod
    def get_rsoccer_robot_speed_max_radians_seconds():
        configuration = Configuration._get_rsoccer_configuration()
        return configuration["robot"]["speed"]["max-radians-seconds"]
    
    @staticmethod
    def get_rsoccer_robot_speed_dead_zone_meters_seconds():
        configuration = Configuration._get_rsoccer_configuration()
        return configuration["robot"]["speed"]["dead-zone-meters-seconds"]
    
    @staticmethod
    def get_rsoccer_robot_width():
        configuration = Configuration._get_rsoccer_configuration()
        return configuration["robot"]["width"]
    
    @staticmethod
    def get_rsoccer_robot_length():
        configuration = Configuration._get_rsoccer_configuration()
        return configuration["robot"]["length"]
    
    @staticmethod
    def get_rsoccer_team_is_yellow_left_team():
        configuration = Configuration._get_rsoccer_configuration()
        return configuration["team"]["is-yellow-left-team"]
    
    @staticmethod
    def get_rsoccer_team_is_yellow_team():
        configuration = Configuration._get_rsoccer_configuration()
        return configuration["team"]["is-yellow-team"]
    
    @staticmethod
    def get_rsoccer_team_blue_number_robots():
        configuration = Configuration._get_rsoccer_configuration()
        return configuration["team"]["blue"]["number-robots"]
    
    @staticmethod
    def get_rsoccer_team_yellow_number_robots():
        configuration = Configuration._get_rsoccer_configuration()
        return configuration["team"]["yellow"]["number-robots"]
    
    @staticmethod
    def get_rsoccer_is_left_team():
        return Configuration.get_rsoccer_team_is_yellow_left_team() \
            == Configuration.get_rsoccer_team_is_yellow_team()
    
    @staticmethod
    def get_rsoccer_training_time_step_seconds():
        configuration = Configuration._get_rsoccer_configuration()
        return configuration["training"]["time-step"]
    
    @staticmethod
    def get_rsoccer_training_episode_duration():
        configuration = Configuration._get_rsoccer_configuration()
        return configuration["training"]["episode-duration"]
    
    @staticmethod
    def get_firasim_control_ip():
        configuration = Configuration._get_firasim_configuration()
        return configuration["control"]["ip"]
    
    @staticmethod
    def get_firasim_control_port():
        configuration = Configuration._get_firasim_configuration()
        return configuration["control"]["port"]
    
    @staticmethod
    def get_firasim_vision_ip():
        configuration = Configuration._get_firasim_configuration()
        return configuration["vision"]["ip"]
    
    @staticmethod
    def get_firasim_vision_port():
        configuration = Configuration._get_firasim_configuration()
        return configuration["vision"]["port"]
    
    @staticmethod
    def get_firasim_vision_buffer_size():
        configuration = Configuration._get_firasim_configuration()
        return configuration["vision"]["buffer"]["size"]
    
    @staticmethod
    def get_firasim_robot_wheel_radius():
        configuration = Configuration._get_firasim_configuration()
        return configuration["robot"]["wheel"]["radius"]
    
    @staticmethod
    def get_firasim_robot_speed_max_radians_seconds():
        configuration = Configuration._get_firasim_configuration()
        return configuration["robot"]["speed"]["max-radians-seconds"]
    
    @staticmethod
    def get_firasim_robot_width():
        configuration = Configuration._get_firasim_configuration()
        return configuration["robot"]["width"]
    
    @staticmethod
    def get_firasim_robot_length():
        configuration = Configuration._get_firasim_configuration()
        return configuration["robot"]["length"]
    
    @staticmethod
    def get_firasim_team_is_yellow_left_team():
        configuration = Configuration._get_firasim_configuration()
        return configuration["team"]["is-yellow-left-team"]
    
    @staticmethod
    def get_firasim_team_is_yellow_team():
        configuration = Configuration._get_firasim_configuration()
        return configuration["team"]["is-yellow-team"]
    
    @staticmethod
    def get_firasim_is_left_team():
        return Configuration.get_firasim_team_is_yellow_left_team() \
            == Configuration.get_firasim_team_is_yellow_team()
    
    @staticmethod
    def get_firasim_team_blue_number_robots():
        configuration = Configuration._get_firasim_configuration()
        return configuration["team"]["blue"]["number-robots"]
    
    @staticmethod
    def get_firasim_team_yellow_number_robots():
        configuration = Configuration._get_firasim_configuration()
        return configuration["team"]["yellow"]["number-robots"]
    
    @staticmethod
    def _get_referee_configuration():
        configuration = Configuration._get_configuration()
        return configuration["referee"]
    
    @staticmethod
    def get_referee_ip():
        configuration = Configuration._get_referee_configuration()
        return configuration["ip"]
    
    @staticmethod
    def get_referee_port():
        configuration = Configuration._get_referee_configuration()
        return configuration["port"]
    
    @staticmethod
    def get_referee_buffer_size():
        configuration = Configuration._get_referee_configuration()
        return configuration["buffer"]["size"]
    
    @staticmethod
    def _get_replacer_configuration():
        configuration = Configuration._get_configuration()
        return configuration["replacer"]
    
    @staticmethod
    def get_replacer_ip():
        configuration = Configuration._get_replacer_configuration()
        return configuration["ip"]
    
    @staticmethod
    def get_replacer_port():
        configuration = Configuration._get_replacer_configuration()
        return configuration["port"]
    
    @staticmethod
    def get_field_length():
        configuration = Configuration._get_configuration()
        return configuration["field"]["length"]
    
    @staticmethod
    def get_field_width():
        configuration = Configuration._get_configuration()
        return configuration["field"]["width"]
    
    @staticmethod
    def get_field_goal_width():
        configuration = Configuration._get_configuration()
        return configuration["field"]["goal"]["width"]
    
    @staticmethod
    def get_field_goal_depth():
        configuration = Configuration._get_configuration()
        return configuration["field"]["goal"]["depth"]
    
    @staticmethod
    def get_field_goal_area_length():
        configuration = Configuration._get_configuration()
        return configuration["field"]["goal-area"]["length"]
    
    @staticmethod
    def get_field_goal_area_width():
        configuration = Configuration._get_configuration()
        return configuration["field"]["goal-area"]["width"]
    
    @staticmethod
    def get_field_ball_radius():
        configuration = Configuration._get_configuration()
        return configuration["field"]["ball"]["radius"]
    
    @staticmethod
    def get_model_attacker_path():
        configuration = Configuration._get_configuration()
        return configuration["model"]["attacker"]["path"]