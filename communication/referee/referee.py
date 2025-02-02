from communication.protobuf.referee import vssref_command_pb2
from communication.receiver.socket_receiver import SocketReceiver
from configuration.configuration import Configuration
from lib.domain.referee_message import RefereeMessage
from lib.utils.referee_utils import RefereeUtils
import select

class Referee(SocketReceiver):
    def __init__(self, referee_message: RefereeMessage):
        super(Referee, self).__init__(
            Configuration.referee_ip,
            Configuration.referee_port,
            Configuration.referee_buffer_size
        )

        self.receiver_socket.setblocking(False)
        self.referee_message = referee_message
        self.protobuf_command = vssref_command_pb2.VSSRef_Command()

    def update(self):
        ready_to_read, _, _ = select.select([self.receiver_socket], [], [], 0)
        if ready_to_read:
            try:
                data = super().receive()
                self.protobuf_command.ParseFromString(data)
                RefereeUtils.set_referee_message(self.referee_message, self.protobuf_command)
            except Exception:
                pass