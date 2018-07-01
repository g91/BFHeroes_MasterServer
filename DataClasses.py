class Client:
    userID = 0
    personaID = 0
    nuid = ""
    personaName = ""

    accountSessionKey = ""
    personaSessionKey = ""

    plasmaPacketID = 0
    playerID = 0  # PID on server

    filteredServers = 0

    locale = ""

    ipAddr = None
    networkInt = None
    theaterInt = None
    IsUp = False

    ping_timer = None
    memcheck_timer = None


class Server:
    userID = 0
    personaID = 0
    nuid = ""
    personaName = ""

    accountSessionKey = ""
    personaSessionKey = ""

    serverData = None

    plasmaPacketID = 0
    startedUBRAs = 0

    clientVersion = ""
    gameID = 0
    joiningPlayers = 0
    activePlayers = 0
    newPlayerID = 0
    connectedPlayers = []

    validServers = {}

    validPersonas = {}

    ipAddr = None
    networkInt = None
    theaterInt = None
    IsUp = False

    ping_timer = None
    memcheck_timer = None
