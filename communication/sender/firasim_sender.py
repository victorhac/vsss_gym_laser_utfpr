
from communication.protobuf.firasim import command_pb2, packet_pb2
from communication.sender.socket_sender import SocketSender
from configuration.configuration import Configuration
from lib.command.team_command import TeamCommand

class FirasimSender(SocketSender):
    def __init__(self):
        super(FirasimSender, self).__init__(
            Configuration.firasim_control_ip,
            Configuration.firasim_control_port)

    def transmit(self, packet):
        super().transmit(packet)

    def transmit_robot(
        self,
        robot_id: int,
        left_speed: float,
        right_speed: float,
        is_yellow_team: bool
    ):
        packet = self._fill_robot_command_packet(
            robot_id,
            left_speed,
            right_speed,
            is_yellow_team
        )

        self.transmit(packet)

    def _fill_robot_command_packet(
        self,
        robot_id: int,
        left_speed: float,
        right_speed: float,
        is_yellow_team: bool
    ):
        packet = command_pb2.Commands()

        robot = packet.robot_commands.add()
        robot.id = robot_id
        robot.yellowteam = is_yellow_team
        robot.wheel_left = left_speed
        robot.wheel_right = right_speed

        packet = packet_pb2.Packet()
        packet.cmd.CopyFrom(packet)

        return packet

    def transmit_team(self, team_command : TeamCommand):
        packet = self._fill_team_command_packet(team_command)
        self.transmit(packet)

    def _fill_team_command_packet(self, team_command: TeamCommand):
        command_packet = command_pb2.Commands()

        for i in range(len(team_command.commands)):
            command = command_packet.robot_commands.add()
            command.id = i
            command.yellowteam = team_command.is_yellow
            command.wheel_left = team_command.commands[i].left_speed
            command.wheel_right = team_command.commands[i].right_speed

        packet = packet_pb2.Packet()
        packet.cmd.CopyFrom(command_packet)

        return packet
