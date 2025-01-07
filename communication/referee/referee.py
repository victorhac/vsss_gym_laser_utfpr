from communication.protobuf.referee import vssref_command_pb2
from communication.receiver.socket_receiver import SocketReceiver
from configuration.configuration import Configuration
from lib.domain.referee_message import RefereeMessage
from lib.utils.referee_utils import RefereeUtils

class Referee(SocketReceiver):
    def __init__(self):
        super(Referee, self).__init__(
            Configuration.get_referee_ip(),
            Configuration.get_referee_port(),
            Configuration.get_referee_buffer_size()
        )

        self.receiver_socket.setblocking(False)
        self.last_rcv_data = RefereeMessage()

    def receive(self):
        try:
            data = super().receive()
            decoded_data = vssref_command_pb2.VSSRef_Command().FromString(data)
            referee_message = RefereeUtils.get_referee_message(decoded_data)
            self.last_rcv_data = referee_message
        except BlockingIOError:
            referee_message = self.last_rcv_data

        return referee_message
