from communication.protobuf.referee import vssref_command_pb2
from communication.receiver.socket_receiver import SocketReceiver
from configuration.configuration import Configuration
from lib.domain.referee_message import RefereeMessage
from lib.utils.referee_utils import RefereeUtils
import select

class Referee(SocketReceiver):
    def __init__(self):
        super(Referee, self).__init__(
            Configuration.referee_ip,
            Configuration.referee_port,
            Configuration.referee_buffer_size
        )

        self.receiver_socket.setblocking(False)
        self.last_received_message = RefereeMessage()
        self.protobuf_command = vssref_command_pb2.VSSRef_Command()

    def receive(self):
        ready_to_read, _, _ = select.select([self.receiver_socket], [], [], 0)
        if ready_to_read:
            try:
                data = super().receive()
                self.protobuf_command.ParseFromString(data)
                referee_message = RefereeUtils.get_referee_message(self.protobuf_command)
                self.last_received_message = referee_message
            except Exception:
                referee_message = self.last_received_message
        else:
            referee_message = self.last_received_message

        return referee_message