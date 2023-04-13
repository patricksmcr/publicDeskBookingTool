from datetime import datetime, timedelta # noqa
import json
from src.models import User, Session
from src.utils.databaseUtils import createConnection, executeSqlCommand, insertInto # noqa
from configparser import RawConfigParser


def createDb():
    connection = createConnection("src/resources/database.db")

    sqlFile = open("src/resources/dbCreationScript.json")
    sqlJson = json.load(sqlFile)
    sqlFile.close()

    for sqlObject in sqlJson:
        print(sqlObject["description"])
        executeSqlCommand(connection, sqlObject["sql"])

    config = RawConfigParser()
    config.read('admin.config')
    configDict = dict(config.items("ADMIN VARIABLES"))

    insertInto(connection, User(configDict['email'], configDict['name'], True, configDict['hash']))
    insertInto(connection, Session("adminToken", configDict['email'], datetime.now() + timedelta(hours=6)))

    connection.close()
