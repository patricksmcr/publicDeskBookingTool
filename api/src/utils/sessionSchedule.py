from datetime import datetime
import time
from threading import Thread
from src.models.session import Session
from src.utils.databaseUtils import createConnection, deleteFrom


def checkExpiryDates():
    connection = createConnection("src/resources/database.db")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    deleteFrom(connection, Session, "ExpireTime < '" + now+"'")


def sessionSchedule():
    while True:
        checkExpiryDates()
        time.sleep(60)


def startSeessionSchedule():
    daemon = Thread(target=sessionSchedule, daemon=True, name="sessionSchedule")
    daemon.start()
