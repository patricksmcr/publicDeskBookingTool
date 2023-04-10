import json
from src.utils.databaseUtils import createConnection, executeSqlCommand # noqa


connection = createConnection("src/resources/database.db")

sqlFile = open("src/resources/dbCreationScript.json")
sqlJson = json.load(sqlFile)
sqlFile.close()

for sqlObject in sqlJson:
    print(sqlObject["description"])
    executeSqlCommand(connection, sqlObject["sql"])
connection.close()
import src.utils.dbPopulate  # noqa
