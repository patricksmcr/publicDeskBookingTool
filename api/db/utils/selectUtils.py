import sys  # noqa
sys.path.append("../../")  # noqa
from api.db.utils.databaseUtils import selectFrom
from api.db.models.booking import Booking
from api.db.models.session import Session
from api.db.models.desk import Desk
from api.db.models.user import User


# User select
def getUsers(connection, email):
    return selectFrom(connection, User, "Email = '{}'".format(email))


def getAllUsers(connection):
    return selectFrom(connection, User, "Email IS NOT NULL")


# Booking select
def getUserBookings(connection, email):
    return selectFrom(connection, Booking, "Email = '{}'".format(email))


def getDeskBookings(connection, deskId):
    return selectFrom(connection, Booking, "DeskId = {}".format(deskId))


def getDateBookings(connection, date):
    return selectFrom(connection, Booking, "Date = '{}'".format(date))


def getBooking(connection, bookingId):
    return selectFrom(connection, Booking, "BookingId = '{}'".format(bookingId))[0]


# Desk select
def getAvailableDesks(connection, date):
    bookings = selectFrom(connection, Booking, "Date='{}'".format(date))
    unavailableDesks = ""
    for booking in bookings:
        unavailableDesks = unavailableDesks + " "+str(booking.deskId)+","
    return selectFrom(connection, Desk, "DeskId NOT IN ({})".format(unavailableDesks[:-1]))


# Session select
def getSession(connection, token):
    return selectFrom(connection, Session, "Token = '{}'".format(token))


def getSessionUser(connection, token):
    return getUsers(connection, getSession(connection, token)[0].email)
