from datetime import datetime, timedelta
from db.models.session import Session
from db.models.desk import Desk
from db.models.booking import Booking
from db.models.user import User
from db.utils.databaseUtils import createConnection, insertInto
import sys
sys.path.append("../")

connection = createConnection("db/resources/database.db")

insertInto(connection, User("user1@email.com", "person 1", True, "1216985755"))
insertInto(connection, User("user2@email.com",
           "person 2", False, "1216985755"))
insertInto(connection, User("user3@email.com",
           "person 3", False, "1216985755"))
insertInto(connection, User("user4@email.com",
           "person 4", False, "1216985755"))
insertInto(connection, User("user5@email.com",
           "person 5", False, "1216985755"))

insertInto(connection, Desk(None, 1))
insertInto(connection, Desk(None, 1))
insertInto(connection, Desk(None, 1))
insertInto(connection, Desk(None, 2))
insertInto(connection, Desk(None, 2))

insertInto(connection, Booking(None, "user1@email.com", 1, "2000-01-1"))
insertInto(connection, Booking(None, "user2@email.com", 2, "2000-01-1"))
insertInto(connection, Booking(None, "user3@email.com", 4, "2000-01-1"))
insertInto(connection, Booking(None, "user4@email.com", 1, "2000-01-2"))
insertInto(connection, Booking(None, "user5@email.com", 3, "2000-01-2"))
insertInto(connection, Booking(None, "user1@email.com", 2, "2000-01-2"))
insertInto(connection, Booking(None, "user2@email.com", 1, "2000-01-3"))
insertInto(connection, Booking(None, "user3@email.com", 4, "2000-01-3"))
insertInto(connection, Booking(None, "user4@email.com", 2, "2000-01-3"))

insertInto(connection, Session("token1", "user1@email.com",
           datetime.now() + timedelta(hours=6)))
insertInto(connection, Session("token2", "user2@email.com",
           datetime.now() + timedelta(hours=5)))
insertInto(connection, Session("token3", "user3@email.com",
           datetime.now() + timedelta(hours=7)))
insertInto(connection, Session("token4", "user4@email.com",
           datetime.now() + timedelta(hours=6)))

connection.close()
