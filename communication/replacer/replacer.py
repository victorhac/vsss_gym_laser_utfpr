from communication.sender.socket_sender import SocketSender
from configuration.configuration import Configuration
from lib.comm.protocols import vssref_placement_pb2

class Replacer(SocketSender):
    def __init__(
        self,
        is_yellow_team: bool
    ):
        super(Replacer, self).__init__(
            Configuration.get_replacer_ip(),
            Configuration.get_replacer_port())

        self.is_yellow_team = is_yellow_team

    def transmit(self, packet):
        super().transmit(packet)

    def place_team(self, replacement_list):
        packet = self._fill_robot_command_packet(replacement_list)
        self.transmit(packet)

    def _fill_robot_command_packet(self, replacement_list):
        placement_packet = vssref_placement_pb2.VSSRef_Placement()
        placement_packet.world.teamColor = int(self.is_yellow_team)

        for desired_placement in replacement_list:
            entity_data, robot_id = desired_placement

            robot = placement_packet.world.robots.add()
            robot.robot_id = int(robot_id)
            robot.x = entity_data.position.x
            robot.y = entity_data.position.y
            robot.orientation = entity_data.position.theta

        return placement_packet
