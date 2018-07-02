# -*- coding: utf-8 -*-

from base64 import b64decode

from Globals import Clients
from Database import Database
from Utilities.Packet import Packet
from Utilities.RandomStringGenerator import GenerateRandomString

db = Database()


def HandleNuLogin(self, data):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "NuLogin")

    password = data.get('PacketData', "password")

    try:
        loginStatus = self.CONNOBJ.validServers[password]
        loginStatus = True
    except:
        self.logger_err.new_message("[Login] Server wanted to login with incorrect login data!", 1)
        loginStatus = False

    if loginStatus:
        self.CONNOBJ.accountSessionKey = db.registerSession()
        self.CONNOBJ.userID = self.CONNOBJ.validServers[password]
        self.CONNOBJ.nuid = password

        toSend.set("PacketData", "lkey", self.CONNOBJ.accountSessionKey)
        toSend.set("PacketData", "nuid", "")

        toSend.set("PacketData", "profileId", str(self.CONNOBJ.userID))
        toSend.set("PacketData", "userId", str(self.CONNOBJ.userID))

        self.logger.new_message("[Login] Server " + password + " logged in successfully!", 1)
    else:
        toSend.set("PacketData", "localizedMessage", "The password the user specified is incorrect")
        toSend.set("PacketData", "errorContainer.[]", "0")
        toSend.set("PacketData", "errorCode", "122")

        self.logger_err.new_message("[Login] Server " + password + " specified incorrect password!", 1)

    Packet(toSend).send(self, "acct", 0xC0000000, self.CONNOBJ.plasmaPacketID)


def HandleNuGetPersonas(self):
    """ Get personas associated with account """

    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "NuGetPersonas")
    toSend.set("PacketData", "personas.[]", "1")

    userID = self.CONNOBJ.userID

    if userID == 1:
        toSend.set("PacketData", "personas.0", "BFHeroesServerPC")

    Packet(toSend).send(self, "acct", 0x80000000, self.CONNOBJ.plasmaPacketID)


def HandleNuLoginPersona(self, data):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "NuLoginPersona")

    requestedPersonaName = data.get("PacketData", "name")

    if requestedPersonaName in self.CONNOBJ.validPersonas:
        self.CONNOBJ.personaID = self.CONNOBJ.validPersonas[requestedPersonaName]
        self.CONNOBJ.personaSessionKey = db.registerSession()
        self.CONNOBJ.personaName = requestedPersonaName

        toSend.set("PacketData", "lkey", self.CONNOBJ.personaSessionKey)
        toSend.set("PacketData", "profileId", str(self.CONNOBJ.personaID))
        toSend.set("PacketData", "userId", str(self.CONNOBJ.personaID))

        self.logger.new_message("[Persona] Server " + self.CONNOBJ.nuid + " just logged as " + requestedPersonaName, 1)
    else:
        toSend.set("PacketData", "localizedMessage", "The user was not found")
        toSend.set("PacketData", "errorContainer.[]", "0")
        toSend.set("PacketData", "errorCode", "101")
        self.logger_err.new_message("[Persona] Server " + self.CONNOBJ.nuid + " wanted to login as " + requestedPersonaName + " but this persona cannot be found!", 1)

    Packet(toSend).send(self, "acct", 0xC0000000, self.CONNOBJ.plasmaPacketID)


def HandleNuGetAccount(self):
    """ Get Account Info """
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "NuGetAccount")

    userID = self.CONNOBJ.userID

    toSend.set("PacketData", "heroName", self.CONNOBJ.nuid)
    toSend.set("PacketData", "nuid", self.CONNOBJ.nuid)
    toSend.set("PacketData", "DOBDay", "1")
    toSend.set("PacketData", "DOBMonth", "1")
    toSend.set("PacketData", "DOBYear", "2017")
    toSend.set("PacketData", "userID", str(userID))
    toSend.set("PacketData", "globalOptin", "0")
    toSend.set("PacketData", "thidPartyOptin", "0")
    toSend.set("PacketData", "language", "enUS")
    toSend.set("PacketData", "country", "US")

    Packet(toSend).send(self, "acct", 0xC0000000, self.CONNOBJ.plasmaPacketID)


def HandleNuLookupUserInfo(self, data):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "NuLookupUserInfo")

    personaName = data.get("PacketData", "userInfo.0.userName")

    toSend.set("PacketData", "userInfo.[]", "1")
    toSend.set("PacketData", "userInfo.0.userName", personaName)
    toSend.set("PacketData", "userInfo.0.namespace", "MAIN")
    toSend.set("PacketData", "userInfo.0.userId", str(self.CONNOBJ.personaID))
    toSend.set("PacketData", "userInfo.0.masterUserId", str(self.CONNOBJ.userID))

    Packet(toSend).send(self, "acct", 0xC0000000, self.CONNOBJ.plasmaPacketID)


def ReceivePacket(self, data, txn):
    if txn == 'NuLogin':
        HandleNuLogin(self, data)
    elif txn == 'NuGetPersonas':
        HandleNuGetPersonas(self)
    elif txn == 'NuLoginPersona':
        HandleNuLoginPersona(self, data)
    elif txn == 'NuGetAccount':
        HandleNuGetAccount(self)
    elif txn == 'NuLookupUserInfo':
        HandleNuLookupUserInfo(self, data)
    else:
        self.logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown acct message (' + txn + ")", 2)
