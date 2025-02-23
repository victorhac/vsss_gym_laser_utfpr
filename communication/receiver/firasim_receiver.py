from communication.protobuf.firasim import packet_pb2
from communication.receiver.socket_receiver import SocketReceiver
from configuration.configuration import Configuration
from lib.utils.field_utils import FieldUtils
from lib.utils.firasim_utils import FIRASimUtils

from lib.domain.field import Field
from lib.domain.robot import Robot
from lib.domain.ball import Ball

import json
from google.protobuf.json_format import MessageToJson

from lib.utils.geometry_utils import GeometryUtils

class FirasimReceiver(SocketReceiver):
    def __init__(
        self,
        is_yellow_team: bool,
        field: Field
    ):
        super(FirasimReceiver, self).__init__(
            Configuration.firasim_vision_ip,
            Configuration.firasim_vision_port,
            Configuration.firasim_vision_buffer_size)

        self.is_yellow_team = is_yellow_team
        self.field = field
        self.is_left_team = \
            Configuration.firasim_team_is_yellow_left_team == is_yellow_team

    def _receive_dict(self):
        data = self.receive()
        decoded_data = packet_pb2.Environment().FromString(data)
        return json.loads(MessageToJson(decoded_data.frame))

    def update(self):
        vision_data_dict = self._receive_dict()
        self._field_data_from_dict(self.field, vision_data_dict)

    def _entity_from_dict(
        self,
        entity: (Robot | Ball),
        data_dict: dict
    ):
        entity.position.x, entity.position.y = \
            FIRASimUtils.correct_position(
                data_dict.get('x', 0), 
                data_dict.get('y', 0),
                self.is_left_team)

        entity.position.theta = \
            GeometryUtils.correct_angle(
                data_dict.get('orientation', 0),
                self.is_left_team)

        entity.velocity.x, entity.velocity.y = \
            FIRASimUtils.correct_speed(
                data_dict.get('vx', 0),
                data_dict.get('vy', 0),
                self.is_left_team)

        entity.velocity.theta = data_dict.get('vorientation', 0)
        entity.active = True

    def _field_data_from_dict(
        self,
        field: Field,
        raw_data_dict: dict
    ):        
        if self.is_yellow_team:
            team_list_of_dicts = raw_data_dict.get('robotsYellow')
            foes_list_of_dicts = raw_data_dict.get('robotsBlue')
        else:
            team_list_of_dicts = raw_data_dict.get('robotsBlue')
            foes_list_of_dicts = raw_data_dict.get('robotsYellow')

        if 'ball' in raw_data_dict:
            self._entity_from_dict(field.ball, raw_data_dict['ball'])

        self._team_from_dict(
            team_list_of_dicts,
            self.field._robots
        )

        self._team_from_dict(
            foes_list_of_dicts,
            self.field._foes
        )

    def _is_robot_inside_field(
        self,
        robot: Robot
    ):
        return FieldUtils.is_inside_field(
            robot.position.x,
            robot.position.y,
            Configuration.field_length,
            Configuration.field_width,
            Configuration.field_goal_width,
            Configuration.field_goal_depth
        )

    def _team_from_dict(
        self,
        team_list_of_dicts: list,
        robots: list
    ):
        robot_ids = [robot.get('robotId', 0) for robot in team_list_of_dicts]

        for i in range(len(team_list_of_dicts)):
            data_dict = team_list_of_dicts[i]
            robot_id = data_dict.get('robotId', 0)
            self._entity_from_dict(robots[robot_id], data_dict)

        for i in range(len(robots)):
            robot = robots[i]
            if i not in robot_ids or not self._is_robot_inside_field(robot):
                robot.active = False
