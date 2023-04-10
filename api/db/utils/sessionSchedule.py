from datetime import datetime
import schedule
import time
from db.models.session import Session
from db.utils.databaseUtils import createConnection, deleteFrom


def checkExpiryDates():
    connection = createConnection("db/resources/database.db")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    deleteFrom(connection, Session, "ExpireTime < '" + now+"'")


schedule.every(5).minutes.do(checkExpiryDates)

while True:
    schedule.run_pending()
    time.sleep(1)
