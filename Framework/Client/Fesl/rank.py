from Database import Database
from Utilities.Packet import Packet

db = Database()


def HandleGetStats(self, data):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "GetStats")

    requestedKeysNumber = int(data.get("PacketData", "keys.[]"))
    requestedKeys = []

    isUser = False
    for i in range(requestedKeysNumber):
        key = data.get("PacketData", "keys." + str(i))
        if key == 'c_ltm' or key == 'c_slm' or key == 'c_tut':
            isUser = True

        requestedKeys.append(key)

    if isUser:
        keysValues = db.GetStats(self.CONNOBJ.userID, "account", requestedKeys)
    else:
        keysValues = db.GetStats(data.get('PacketData', 'owner'), "persona", requestedKeys)

    for i in range(len(requestedKeys)):
        toSend.set("PacketData", "stats." + str(i) + ".key", keysValues[i]['name'])
        toSend.set("PacketData", "stats." + str(i) + ".value", str(keysValues[i]['value']))
        toSend.set("PacketData", "stats." + str(i) + ".text", keysValues[i]['text'])

    toSend.set("PacketData", "stats.[]", str(requestedKeysNumber))

    Packet(toSend).send(self, "rank", 0xC0000000, self.CONNOBJ.plasmaPacketID)


def HandleUpdateStats(self, data):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "UpdateStats")

    users = int(data.get("PacketData", "u.[]"))

    for user in range(users):
        owner = int(data.get("PacketData", "u." + str(user) + ".o"))

        statsToUpdate = int(data.get("PacketData", "u." + str(user) + ".s.[]"))

        for stat in range(statsToUpdate):
            key = str(data.get("PacketData", "u." + str(user) + ".s." + str(stat) + ".k"))
            value = str(data.get("PacketData", "u." + str(user) + ".s." + str(stat) + ".v"))
            text = str(data.get("PacketData", "u." + str(user) + ".s." + str(stat) + ".t"))

            if key == 'c_ltm' or key == 'c_slm' or key == 'c_tut':
                db.updateStat(owner, "account", key, value, text)
            else:
                db.updateStat(owner, "persona", key, value, text)

    Packet(toSend).send(self, "rank", 0xC0000000, self.CONNOBJ.plasmaPacketID)


def ReceivePacket(self, data, txn):
    if txn == 'GetStats':
        HandleGetStats(self, data)
    elif txn == 'UpdateStats':
        HandleUpdateStats(self, data)
    else:
        self.logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown rank message (' + txn + ")", 2)
