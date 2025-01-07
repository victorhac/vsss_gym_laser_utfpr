import json
from google.protobuf.json_format import MessageToJson

from communication.protobuf.referee import vssref_command_pb2
from communication.receiver.socket_receiver import SocketReceiver

class RefereeComm(SocketReceiver):
    def __init__(self, referee_ip='224.5.23.2', referee_port=10003):
        super(RefereeComm, self).__init__(referee_ip, referee_port, 1024)
        self.receiver_socket.setblocking(False)
        self.last_rcv_data = {}

    def receive(self):
        try:
            data = super().receive()
            decoded_data = vssref_command_pb2.VSSRef_Command().FromString(data)
            referee_data = json.loads(MessageToJson(decoded_data))
            self.last_rcv_data = referee_data
        except BlockingIOError:
            referee_data = self.last_rcv_data

        return referee_data
