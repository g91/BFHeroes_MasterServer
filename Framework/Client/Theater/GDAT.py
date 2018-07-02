from Globals import Servers
from Utilities.Packet import Packet


def ReceiveRequest(self, data):
    try:
        lobbyID = str(data.get("PacketData", "LID"))
        gameID = str(data.get("PacketData", "GID"))
    except:
        lobbyID = None
        gameID = None

    if lobbyID is not None and gameID is not None:
        server = None

        for srv in Servers:
            if str(srv.serverData.get("ServerData", "LID")) == lobbyID and str(srv.serverData.get("ServerData", "GID")) == gameID:
                server = srv

        toSend = Packet().create()
        toSend.set("PacketData", "TID", str(data.get("PacketData", "TID")))
        toSend.set("PacketData", "LID", lobbyID)
        toSend.set("PacketData", "GID", gameID)

        toSend.set("PacketData", "HU", str(server.personaID))
        toSend.set("PacketData", "HN", str(server.personaName))

        toSend.set("PacketData", "I", server.ipAddr)
        toSend.set("PacketData", "P", str(server.serverData.get("ServerData", "PORT")))  # Port

        toSend.set("PacketData", "N", str(server.serverData.get("ServerData", "NAME")))  # name of server in list
        toSend.set("PacketData", "AP", str(server.activePlayers))  # current number of players on server
        toSend.set("PacketData", "MP", str(server.serverData.get("ServerData", "MAX-PLAYERS")))  # Maximum players on server
        toSend.set("PacketData", "JP", str(server.joiningPlayers))  # Players that are joining the server right now?
        toSend.set("PacketData", "PL", "PC")  # Platform - PC / XENON / PS3

        # Constants
        toSend.set("PacketData", "PW", "0")  # ??? - its certainly not something like "hasPassword"
        toSend.set("PacketData", "TYPE", str(server.serverData.get("ServerData", "TYPE")))  # what type?? constant value - "G"
        toSend.set("PacketData", "J", str(server.serverData.get("ServerData", "JOIN")))  # ??? constant value - "O"

        # Userdata
        toSend.set("PacketData", "B-U-alwaysQueue", str(server.serverData.get("ServerData", "B-U-alwaysQueue")))
        toSend.set("PacketData", "B-U-army_balance", str(server.serverData.get("ServerData", "B-U-army_balance")))
        toSend.set("PacketData", "B-U-army_distribution", str(server.serverData.get("ServerData", "B-U-army_distribution")))
        toSend.set("PacketData", "B-U-avail_slots_national", str(server.serverData.get("ServerData", "B-U-avail_slots_national")))
        toSend.set("PacketData", "B-U-avail_slots_royal", str(server.serverData.get("ServerData", "B-U-avail_slots_royal")))

        toSend.set("PacketData", "B-U-avg_ally_rank", str(server.serverData.get("ServerData", "B-U-avg_ally_rank")))
        toSend.set("PacketData", "B-U-avg_axis_rank", str(server.serverData.get("ServerData", "B-U-avg_axis_rank")))
        toSend.set("PacketData", "B-U-community_name", str(server.serverData.get("ServerData", "B-U-community_name")))
        toSend.set("PacketData", "B-U-data_center", str(server.serverData.get("ServerData", "B-U-data_center")))
        toSend.set("PacketData", "B-U-elo_rank", str(server.serverData.get("ServerData", "B-U-elo_rank")))
        toSend.set("PacketData", "B-U-map", str(server.serverData.get("ServerData", "B-U-map")))
        toSend.set("PacketData", "B-U-percent_full", str(server.serverData.get("ServerData", "B-U-percent_full")))
        toSend.set("PacketData", "B-U-server_ip", str(server.serverData.get("ServerData", "B-U-server_ip")))
        toSend.set("PacketData", "B-U-server_port", str(server.serverData.get("ServerData", "B-U-server_port")))
        toSend.set("PacketData", "B-U-server_state", str(server.serverData.get("ServerData", "B-U-server_state")))
        toSend.set("PacketData", "B-version", str(server.serverData.get("ServerData", "B-version")))

        toSend.set("PacketData", "B-numObservers", str(server.serverData.get("ServerData", "B-numObservers")))  # Observers = spectators? or admins?
        toSend.set("PacketData", "B-maxObservers", str(server.serverData.get("ServerData", "B-maxObservers")))  # Game max observers
        toSend.set("PacketData", "B-U-avail_vips_national", str(server.serverData.get("ServerData", "B-U-avail_vips_national")))
        toSend.set("PacketData", "B-U-avail_vips_royal", str(server.serverData.get("ServerData", "B-U-avail_vips_royal")))
        toSend.set("PacketData", "B-U-easyzone", str(server.serverData.get("ServerData", "B-U-easyzone")))
        toSend.set("PacketData", "B-U-lvl_avg", str(server.serverData.get("ServerData", "B-U-lvl_avg")))
        toSend.set("PacketData", "B-U-lvl_sdv", str(server.serverData.get("ServerData", "B-U-lvl_sdv")))
        toSend.set("PacketData", "B-U-map_name", str(server.serverData.get("ServerData", "B-U-map_name")))
        toSend.set("PacketData", "B-U-punkb", str(server.serverData.get("ServerData", "B-U-punkb")))
        toSend.set("PacketData", "B-U-ranked", str(server.serverData.get("ServerData", "B-U-ranked")))
        toSend.set("PacketData", "B-U-servertype", str(server.serverData.get("ServerData", "B-U-servertype")))

        Packet(toSend).send(self, "GDAT", 0x00000000, 0)
    else:
        toSend = Packet().create()
        toSend.set("PacketData", "TID", str(data.get("PacketData", "TID")))
        Packet(toSend).send(self, "GDAT", 0x00000000, 0)
