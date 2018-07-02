from Database import Database
from Utilities.Packet import Packet

db = Database()


def HandleNuLogin(self, data):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "NuLogin")

    loginInfo = data.get("PacketData", "encryptedInfo")
    loginData = db.loginUser(loginInfo)

    if loginData['UserID'] > 0:  # Got UserID - Login Successful
        self.CONNOBJ.accountSessionKey = loginData['SessionID']
        self.CONNOBJ.userID = loginData['UserID']
        self.CONNOBJ.nuid = loginData['username']

        toSend.set("PacketData", "lkey", loginData['SessionID'])
        toSend.set("PacketData", "nuid", self.CONNOBJ.nuid)

        toSend.set("PacketData", "profileId", str(loginData['UserID']))
        toSend.set("PacketData", "userId", str(loginData['UserID']))

        self.logger.new_message("[Login] User " + self.CONNOBJ.nuid + " logged in successfully!", 1)
    else:  # User not found
        toSend.set("PacketData", "localizedMessage", "The user is not entitled to access this game")
        toSend.set("PacketData", "errorContainer.[]", "0")
        toSend.set("PacketData", "errorCode", "120")

        self.logger_err.new_message("[Login] User tryed to login with expired Session Key", 1)

    Packet(toSend).send(self, "acct", 0xC0000000, self.CONNOBJ.plasmaPacketID)


def HandleNuGetPersonas(self, data):
    """ Get personas associated with account """

    userID = self.CONNOBJ.userID
    personas = db.getUserPersonas(userID)

    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "NuGetPersonas")
    toSend.set("PacketData", "personas.[]", str(len(personas)))

    personaId = 0
    for persona in personas:
        toSend.set("PacketData", "personas." + str(personaId), persona)
        personaId += 1

    Packet(toSend).send(self, "acct", 0xC0000000, self.CONNOBJ.plasmaPacketID)


def HandleNuGetAccount(self):
    """ Get Account Info """
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "NuGetAccount")

    userID = self.CONNOBJ.userID
    accountInfo = db.getAccountInfo(userID)

    if accountInfo is not None:
        toSend.set("PacketData", "heroName", accountInfo['email'])
        toSend.set("PacketData", "nuid", accountInfo['email'])
        toSend.set("PacketData", "DOBDay", str(accountInfo['birthday'].split('-')[2]))
        toSend.set("PacketData", "DOBMonth", str(accountInfo['birthday'].split('-')[1]))
        toSend.set("PacketData", "DOBYear", str(accountInfo['birthday'].split('-')[0]))
        toSend.set("PacketData", "userID", str(userID))
        toSend.set("PacketData", "globalOptin", "0")
        toSend.set("PacketData", "thidPartyOptin", "0")
        toSend.set("PacketData", "language", accountInfo['country'])
        toSend.set("PacketData", "country", accountInfo['country'])

    Packet(toSend).send(self, "acct", 0xC0000000, self.CONNOBJ.plasmaPacketID)


def HandleNuLookupUserInfo(self, data):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "NuLookupUserInfo")

    toLookup = int(data.get("PacketData", "userInfo.[]"))

    count = 0
    for user in range(toLookup):
        username = data.get("PacketData", "userInfo." + str(user) + ".userName")
        info = db.getPersonaInfo(username)

        if info is not False:
            toSend.set("PacketData", "userInfo." + str(count) + ".userName", info['personaName'])
            toSend.set("PacketData", "userInfo." + str(count) + ".userId", info['personaID'])
            toSend.set("PacketData", "userInfo." + str(count) + ".masterUserId", info['userID'])
            toSend.set("PacketData", "userInfo." + str(count) + ".namespace", "MAIN")
        else:
            toSend.set("PacketData", "userInfo." + str(count) + ".userName", username)

        count += 1
    toSend.set("PacketData", "userInfo.[]", str(count))
    Packet(toSend).send(self, "acct", 0xC0000000, self.CONNOBJ.plasmaPacketID)


def HandleNuLoginPersona(self, data):
    """ User logs in with selected Persona """

    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "NuLoginPersona")

    requestedPersonaName = data.get("PacketData", "name")

    personaData = db.loginPersona(self.CONNOBJ.userID, requestedPersonaName)
    if personaData is not None:
        self.CONNOBJ.personaID = personaData['personaId']
        self.CONNOBJ.personaSessionKey = personaData['lkey']
        self.CONNOBJ.personaName = requestedPersonaName

        toSend.set("PacketData", "lkey", personaData['lkey'])
        toSend.set("PacketData", "profileId", str(self.CONNOBJ.personaID))
        toSend.set("PacketData", "userId", str(self.CONNOBJ.personaID))

        self.logger.new_message("[Persona] User " + self.CONNOBJ.nuid + " just logged as " + requestedPersonaName, 1)
    else:
        toSend.set("PacketData", "localizedMessage", "The user was not found")
        toSend.set("PacketData", "errorContainer.[]", "0")
        toSend.set("PacketData", "errorCode", "101")
        self.logger_err.new_message("[Persona] User " + self.CONNOBJ.nuid + " wanted to login as " + requestedPersonaName + " but this persona cannot be found!", 1)

    Packet(toSend).send(self, "acct", 0xC0000000, self.CONNOBJ.plasmaPacketID)


def ReceivePacket(self, data, txn):
    if txn == 'NuLogin':
        HandleNuLogin(self, data)
    elif txn == 'NuGetPersonas':
        HandleNuGetPersonas(self, data)
    elif txn == 'NuGetAccount':
        HandleNuGetAccount(self)
    elif txn == 'NuLookupUserInfo':
        HandleNuLookupUserInfo(self, data)
    elif txn == 'NuLoginPersona':
        HandleNuLoginPersona(self, data)
    else:
        self.logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown acct message (' + txn + ")", 2)
