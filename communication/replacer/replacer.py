from communication.protobuf.referee import vssref_placement_pb2
from communication.sender.socket_sender import SocketSender
from configuration.configuration import Configuration
from lib.command.team_replace_command import TeamReplaceCommand
from lib.utils.referee_utils import RefereeUtils

class Replacer(SocketSender):
    def __init__(self):
        super(Replacer, self).__init__(
            Configuration.replacer_ip,
            Configuration.replacer_port)

    def transmit(self, packet):
        super().transmit(packet)

    def place_team(self, command: TeamReplaceCommand):
        packet = self._fill_robot_command_packet(command)
        self.transmit(packet)

    def _fill_robot_command_packet(self, command: TeamReplaceCommand):
        placement_packet = vssref_placement_pb2.VSSRef_Placement()
        placement_packet.world.teamColor = RefereeUtils\
            .get_protobuf_color_enum(command.is_yellow_team)

        for item in command.robot_replace_commands:
            robot = placement_packet.world.robots.add()
            robot.robot_id = item.robot_id
            robot.x = item.x
            robot.y = item.y
            robot.orientation = item.theta

        return placement_packet
