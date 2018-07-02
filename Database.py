import sqlite3
import sys

from os.path import exists
from time import strftime

from passlib.hash import pbkdf2_sha256

from Config import readFromConfig
from Logger import Log
from Utilities.RandomStringGenerator import GenerateRandomString

logger = Log("Database", "\033[37;1m")
logger_err = Log("Database", "\033[37;1;41m")


class Database(object):
    def __init__(self, showWelcomeMsg=False):
        dbFileLocation = readFromConfig("database", "db_file_path")

        if exists(dbFileLocation):
            if showWelcomeMsg:
                logger.new_message('Connected to database!', 1)
            self.connection = sqlite3.connect(dbFileLocation)
            self.cleanup()
        else:
            logger.new_message('Database file not found! Initializing database...', 1)
            self.connection = sqlite3.connect(dbFileLocation)
            try:
                self.initializeDatabase()
                logger.new_message('Database initialized successfully!', 1)
            except Exception as DBError:
                logger_err.new_message(
                    'There is an problem with initializing database!\nAdditional Error Info:\n' + str(DBError), 1)
                sys.exit(6)

    def initializeDatabase(self):
        tables = [{'Accounts': ['userID integer PRIMARY KEY AUTOINCREMENT UNIQUE', 'EMail string UNIQUE', 'Password string', 'Birthday string', 'Country string']},
                  {'Entitlements': ['userID integer', 'entitlementId integer PRIMARY KEY AUTOINCREMENT UNIQUE', 'entitlementTag string', 'status string']},
                  {'Personas': ['userID integer', 'personaID integer PRIMARY KEY AUTOINCREMENT UNIQUE', 'personaName string']},
                  {'Sessions': ['userID integer UNIQUE', 'sessionKey string UNIQUE']},
                  {'Stats': ['forID integer', 'IDType string', 'key string', 'value integer', 'text string']}]

        cursor = self.connection.cursor()

        for table in tables:
            sql = ""
            for name, columns in table.items():
                if len(sql) == 0:
                    sql = "CREATE TABLE " + name + " ("

                for column in columns:
                    sql += column + ','
                sql = sql[:-1]
                sql += ")"

            cursor.execute(sql)

        self.connection.commit()
        cursor.close()

    def cleanup(self):
        tables = []

        cursor = self.connection.cursor()

        for table in tables:
            cursor.execute("DELETE FROM " + table)

        self.connection.commit()
        cursor.close()

        cursor = self.connection.cursor()

        cursor.execute("VACUUM")

        self.connection.commit()

        cursor.close()

    def registerSession(self):
        session = GenerateRandomString(27) + "."
        return session

    def loginUser(self, sessionKey):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Sessions WHERE sessionKey = ?", (sessionKey,))

        data = cursor.fetchone()
        cursor.close()

        if data is not None:
            userID = data[0]

            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Accounts WHERE userID = ?", (userID,))

            data = cursor.fetchone()

            if data is not None:
                nuid = data[1]
                session = self.registerSession()

                return {'UserID': userID, 'username': nuid, 'SessionID': session}

        return {'UserID': -1}  # Incorrect sessionKey

    def getUserPersonas(self, userID):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Personas WHERE userID = ?", (userID,))

        data = cursor.fetchall()

        if data is None:
            return []

        personas = []
        for persona in data:
            personas.append(persona[2])

        return personas

    def getAccountInfo(self, userID):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Accounts WHERE userID = ?", (userID,))

        data = cursor.fetchone()

        if data is not None:
            return {'email': data[1], 'birthday': data[3], 'country': data[4]}

        return None

    def getPersonaInfo(self, personaName):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Personas WHERE personaName = ?", (personaName,))

        data = cursor.fetchone()

        if data is not None:
            return {'userID': str(data[0]),
                    'personaID': str(data[1]),
                    'personaName': str(data[2])}
        else:
            return False

    def GetStats(self, forID, idType, keys):
        values = []

        for key in keys:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Stats WHERE forID = ? AND IDType = ? AND key = ?", (forID, idType, key,))

            data = cursor.fetchone()

            if data is not None:
                values.append({'name': key, 'value': data[3], 'text': data[4]})
            else:
                values.append({'name': key, 'value': 0.0, 'text': ""})

            self.connection.commit()
            cursor.close()

        return values

    def loginPersona(self, userID, personaName):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Personas WHERE userID = ? AND personaName = ?", (userID, personaName,))

        data = cursor.fetchone()

        if data is None:
            return None
        else:
            personaId = data[0]
            session = self.registerSession()

            return {'lkey': session, 'personaId': personaId}

    def getPersonaName(self, personaID):
        cursor = self.connection.cursor()
        cursor.execute("SELECT personaName FROM Personas WHERE personaID = ?", (personaID,))

        data = cursor.fetchone()

        if data is not None:
            return data[0]
        else:
            return False

    def getUserEntitlements(self, userID):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Entitlements WHERE userID = ?", (userID,))

        data = cursor.fetchall()

        entitlements = []
        if data is not None:
            for entitlement in data:
                entitlements.append({'userId': str(entitlement[0]),
                                     'entitlementId': str(entitlement[1]),
                                     'entitlementTag': str(entitlement[2]).replace(":", "%3a"),
                                     'status': str(entitlement[3])})
        return entitlements

