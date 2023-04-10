import sys
sys.path.append("../")
from api.db.utils.databaseUtils import createConnection  # noqa
from api.db.utils.selectUtils import getUsers, getAllUsers, getAvailableDesks, getBooking, getDateBookings, getDeskBookings, getSession, getSessionUser, getUserBookings # noqa

import api.db.utils.dbCreation  # noqa

connection = createConnection("db/resources/database.db")


def test_selectSingleUser():
    assert len(getUsers(connection, "user1@email.com")) == 1


def test_selectNoUsers():
    assert len(getUsers(connection, "fakeAdress@email.com")) == 0


def test_selectAllUsers():
    assert len(getAllUsers(connection)) == 5


def test_getAvailableDesks():
    assert len(getAvailableDesks(connection, '2000-01-01')) == 2


def test_getBooking():
    assert len(getBooking(connection, '1')) == 1


def test_getUndefinedBooking():
    assert len(getBooking(connection, '999')) == 0


def test_getDateBookings():
    assert len(getDateBookings(connection, '2000-01-01')) == 3


def test__getBookingsOnBookingFreeDay():
    assert len(getDateBookings(connection, '3000-01-01')) == 0


def test_getDeskBookings():
    assert len(getDeskBookings(connection, 1)) == 3


def test_getDeskWithNoBookings():
    assert len(getDeskBookings(connection, 5)) == 0


def test_getSession():
    assert len(getSession(connection, 'token1')) == 1


def test_getInvalidSession():
    assert len(getSession(connection, 'invalidToken')) == 0


def test_getSessionUser():
    assert len(getSessionUser(connection, 'token1')) == 1


def test_getSessionUserInvalidToken():
    assert len(getSessionUser(connection, 'invalidToken')) == 0


def test_getUsersBookings():
    assert len(getUserBookings(connection, 'user1@email.com')) == 2


def test_getUsersBookingsWithNoBookings():
    assert len(getUserBookings(connection, 'unregisterd@email.com')) == 0
