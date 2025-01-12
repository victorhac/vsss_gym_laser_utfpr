import socket
from abc import ABC, abstractmethod

class SocketSender(ABC):
    def __init__(
        self,
        transmitter_ip: str,
        transmitter_port: int
    ):
        self.transmitter_ip = transmitter_ip
        self.transmitter_port = transmitter_port

        self.transmitter_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    @abstractmethod
    def transmit(self, packet):
        data = packet.SerializeToString()
        self.transmitter_socket.sendto(
            data,
            (self.transmitter_ip, self.transmitter_port))
