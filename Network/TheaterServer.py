from Logger import Log
from Utilities.Packet import Packet

from twisted.internet.protocol import Protocol, DatagramProtocol


class TCPHandler(Protocol):
    def __init__(self):
        self.CONNOBJ = None
        self.logger = Log("TheaterServer", "\033[36;1m")
        self.logger_err = Log("TheaterServer", "\033[36;1;41m")

    def connectionMade(self):
        self.ip, self.port = self.transport.client
        self.transport.setTcpNoDelay(True)

        self.logger.new_message("[" + self.ip + ":" + str(self.port) + "] connected", 1)

    def connectionLost(self, reason):
        self.logger.new_message("[" + self.ip + ":" + str(self.port) + "] disconnected ", 1)

        if self.CONNOBJ is not None:
            self.CONNOBJ.IsUp = False
            del self

        return

    def dataReceived(self, data):
        packet_type = data[:4]
        packets = data.split('\n\x00')

        dataObjs = []

        if len(packets) > 2:
            for packet in packets:
                fixedPacketType = packet[:4]
                fixedPacket = packet[12:]

                if len(fixedPacket) == 0:
                    break
                else:
                    dataObjs.append({"data": Packet(fixedPacket + "\n\x00").dataInterpreter(), "type": fixedPacketType})
        else:
            dataObjs.append({"data": Packet(packets[0][12:] + "\n\x00").dataInterpreter(), "type": packet_type})

        self.logger.new_message("[" + self.ip + ":" + str(self.port) + "]<-- " + repr(data), 3)

        for dataObj in dataObjs:
            if dataObj['type'] == None:
                pass
            else:
                self.logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown message type (' + dataObj['type'] + ")", 2)



class UDPHandler(DatagramProtocol):
    def __init__(self):
        self.logger = Log("TheaterServer", "\033[32;1m")
        self.logger_err = Log("TheaterServer", "\033[32;1;41m")

    def datagramReceived(self, datagram, addr):
        packet_type = datagram[:4]
        packet_data = datagram[12:]

        dataObj = Packet(packet_data).dataInterpreter()
        self.logger.new_message("[" + addr[0] + ":" + str(addr[1]) + "]<-- " + repr(datagram), 3)

        if packet_type == None:
            pass
        else:
            self.logger_err.new_message("[" + addr[0] + ":" + str(addr[1]) + "][UDP] Received unknown packet type! (" + packet_type + ")", 2)

