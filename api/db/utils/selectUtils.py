from db.utils.databaseUtils import selectFrom
from db.models.booking import Booking
from db.models.session import Session
from db.models.desk import Desk
from db.models.user import User


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
    return selectFrom(connection, Booking, "BookingId = '{}'".format(bookingId))


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
    try:
        return getUsers(connection, getSession(connection, token)[0].email)
    except Exception:
        return []

