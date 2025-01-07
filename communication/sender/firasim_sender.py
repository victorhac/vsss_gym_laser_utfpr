
from communication.protobuf.firasim import command_pb2, packet_pb2
from communication.sender.socket_sender import SocketSender
from lib.command.team_command import TeamCommand

class FirasimSender(SocketSender):
    def __init__(
        self,
        team_color_yellow: bool,
        team_command: TeamCommand,
        control_ip: str,
        control_port: int
    ):
        super(FirasimSender, self).__init__(control_ip, control_port)

        self.team_color_yellow = team_color_yellow
        self.team_command = team_command

    def transmit(self, packet):
        super().transmit(packet)

    def transmit_robot(self, robot_id, left_speed, right_speed):
        packet = self._fill_robot_command_packet(robot_id, left_speed, right_speed)

        self.transmit(packet)

    def _fill_robot_command_packet(
        self,
        robot_id,
        left_speed,
        right_speed
    ):
        cmd_packet = command_pb2.Commands()

        robot = cmd_packet.robot_commands.add()
        robot.id          = robot_id
        robot.yellowteam  = self.team_color_yellow
        robot.wheel_left  = left_speed
        robot.wheel_right = right_speed

        packet = packet_pb2.Packet()
        packet.cmd.CopyFrom(cmd_packet)

        return packet

    def transmit_team(self, team_cmd : TeamCommand):
        packet = self._fill_team_command_packet(team_cmd)

        self.transmit(packet)

    def update(self):
        self.transmit_team(self.team_command)

    def stop_team(self):
        stop_team_cmd = TeamCommand()
        self.transmit_team(stop_team_cmd)

    def _fill_team_command_packet(self, team_command : TeamCommand):
        cmd_packet = command_pb2.Commands()

        for i in range(len(team_command.commands)):
            cmd = cmd_packet.robot_commands.add()
            cmd.id          = i
            cmd.yellowteam  = self.team_color_yellow
            cmd.wheel_left  = team_command.commands[i].left_speed
            cmd.wheel_right = team_command.commands[i].right_speed

        packet = packet_pb2.Packet()
        packet.cmd.CopyFrom(cmd_packet)

        return packet
