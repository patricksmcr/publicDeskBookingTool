from db.utils.selectUtils import getUsers, getAllUsers, getDateBookings, getDeskBookings, getUserBookings, getAvailableDesks
from db.utils.databaseUtils import createConnection

connection = createConnection("db/resources/database.db")

print(getUsers(connection, "user1@email.com")[0].__dict__)
print(getAllUsers(connection))

print(getUserBookings(connection, "user1@email.com"))
print(getDeskBookings(connection, 1))
print(getDateBookings(connection, "2000-01-1"))

print(getAvailableDesks(connection, "2000-01-1"))
