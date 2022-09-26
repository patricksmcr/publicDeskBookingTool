import sys  # noqa
sys.path.append("../")  # noqa
import json
from api.db.utils.databaseUtils import createConnection, executeSqlCommand


connection = createConnection("db/resources/database.db")

sqlFile = open("db/resources/dbCreationScript.json")
sqlJson = json.load(sqlFile)
sqlFile.close()

for sqlObject in sqlJson:
    print(sqlObject["description"])
    executeSqlCommand(connection, sqlObject["sql"])
connection.close()
import dbPopulate  # noqa
