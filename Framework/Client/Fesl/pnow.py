from Globals import Servers
from Utilities.Packet import Packet


def HandleStart(self, data):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "Start")

    partition = data.get("PacketData", "partition.partition")

    toSend.set("PacketData", "id.id", "1")
    toSend.set("PacketData", "id.partition", partition)

    self.logger.new_message("[Matchmaking] User started matchmaking!", 2)
    Packet(toSend).send(self, "pnow", 0xC0000000, self.CONNOBJ.plasmaPacketID)

    Status(self, partition)


def Status(self, partition):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "Status")

    self.logger.new_message("[Matchmaking] Sending matchmaking status...", 1)

    toSend.set("PacketData", "id.id", "1")
    toSend.set("PacketData", "id.partition", partition)
    toSend.set("PacketData", "sessionState", "COMPLETE")
    toSend.set("PacketData", "props.{}.[]", "2")
    toSend.set("PacketData", "props.{resultType}", "JOIN")

    # Get Latest Game (There is no Matchmaking system... Yet) TODO: Matchmaking system

    try:
        selectedGame = Servers[-1]
    except:
        selectedGame = None

    if selectedGame is not None:
        toSend.set("PacketData", "props.{games}.0.lid", "1")
        toSend.set("PacketData", "props.{games}.0.fit", "1001")
        toSend.set("PacketData", "props.{games}.0.gid", str(selectedGame.GameID))
        toSend.set("PacketData", "props.{games}.[]", "1")

        self.logger.new_message("[Matchmaking] Matchmaking finished", 1)
    else:
        toSend.set("PacketData", "props.{games}.[]", "0")

    Packet(toSend).send(self, "pnow", 0x80000000, self.CONNOBJ.plasmaPacketID)


def ReceiveRequest(self, data, txn):
    if txn == 'Start':
        HandleStart(self, data)
    else:
        self.logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown pnow message (' + txn + ")", 2)
