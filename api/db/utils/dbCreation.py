import json
import sys
sys.path.append("../")
from api.db.utils.databaseUtils import createConnection, executeSqlCommand # noqa


connection = createConnection("db/resources/database.db")

sqlFile = open("db/resources/dbCreationScript.json")
sqlJson = json.load(sqlFile)
sqlFile.close()

for sqlObject in sqlJson:
    print(sqlObject["description"])
    executeSqlCommand(connection, sqlObject["sql"])
connection.close()
import api.db.utils.dbPopulate  # noqa
