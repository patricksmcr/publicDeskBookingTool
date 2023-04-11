import json
from src.models import User
from src.utils.databaseUtils import createConnection, executeSqlCommand, insertInto # noqa


def createDb():
    connection = createConnection("src/resources/database.db")

    sqlFile = open("src/resources/dbCreationScript.json")
    sqlJson = json.load(sqlFile)
    sqlFile.close()

    for sqlObject in sqlJson:
        print(sqlObject["description"])
        executeSqlCommand(connection, sqlObject["sql"])
    
    insertInto(connection, User("admin@email.com", "person 1", True, "1216985755"))
    connection.close()
