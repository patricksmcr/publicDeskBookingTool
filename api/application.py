import sys  # noqa
sys.path.append("../")  # noqa
import secrets
from db.utils import selectUtils
from api.db.utils.databaseUtils import createConnection, deleteFrom, insertInto, updateRecord
from flask import Flask, request
from flask_cors import CORS
from api.sessionUtils import validateSession
from api.db.utils.selectUtils import getSession, getSessionUser, getUsers
from api.jsonUtils import objectArrayToJson
from api.db.models.booking import Booking
from api.db.models.session import Session
from api.db.models.user import User
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)


connection = createConnection("db/resources/database.db")


# Booking routes
@app.route('/getUserBookings', methods=["POST"])
def getUserBookings():
    if validateSession(connection, request.get_json()["token"]):
        return objectArrayToJson(selectUtils.getUserBookings(connection, request.get_json()["email"]))
    else:
        return "Session has expired or does not exist", 401


@app.route('/getDeskBookings', methods=["POST"])
def getDeskBookings():
    if validateSession(connection, request.get_json()["token"]):
        return objectArrayToJson(selectUtils.getDeskBookings(connection, request.get_json()["deskId"]))
    else:
        return "Session has expired or does not exist", 401


@app.route('/getDateBookings', methods=["POST"])
def getDateBookings():
    if validateSession(connection, request.get_json()["token"]):
        return objectArrayToJson(selectUtils.getDateBookings(connection, request.get_json()["date"]))
    else:
        return "Session has expired or does not exist", 401


@app.route('/createBooking', methods=["POST"])
def createBookings():
    requestJson = request.get_json()
    if validateSession(connection, requestJson["token"]):
        availableDesks = selectUtils.getAvailableDesks(
            connection, requestJson["date"])
        email = getSessionUser(
            connection, request.get_json()["token"])[0].email
        for desk in availableDesks:
            print(desk.deskId)
            if desk.deskId == int(requestJson["deskId"]):
                insertInto(connection, Booking(
                    None, email, requestJson["deskId"], requestJson["date"]))
                return "Booking added", 200
        return "Failed to add booking", 400
    else:
        return "Session has expired or does not exist", 401


@app.route('/createAdminBooking', methods=["POST"])
def createAdminBookings():
    requestJson = request.get_json()
    if validateSession(connection, requestJson["token"]):
        availableDesks = selectUtils.getAvailableDesks(
            connection, requestJson["date"])
        admin = getSessionUser(connection, request.get_json()["token"])[0]
        if admin.isAdmin == 'False':
            return "Permission denied", 400
        for desk in availableDesks:
            print(desk.deskId)
            if desk.deskId == int(requestJson["deskId"]):
                insertInto(connection, Booking(
                    None, requestJson["email"], requestJson["deskId"], requestJson["date"]))
                return "Booking added", 200
        return "Failed to add booking", 400
    else:
        return "Session has expired or does not exist", 401


@app.route('/deleteBooking', methods=["POST"])
def deleteBooking():
    requestJson = request.get_json()
    if validateSession(connection, requestJson["token"]):
        booking = selectUtils.getBooking(connection, requestJson["bookingId"])
        user = selectUtils.getSessionUser(connection, requestJson["token"])[0]
        if booking.email == user.email:
            deleteFrom(connection, Booking, "BookingId = {}".format(
                requestJson["bookingId"]))
            return "Deleted booking", 200
        elif user.isAdmin == 'True':
            deleteFrom(connection, Booking, "BookingId = {}".format(
                requestJson["bookingId"]))
            return "Deleted booking", 200
        return "Permission Denied", 400
    else:
        return "Session has expired or does not exist", 401


# Desk routes
@app.route('/availableDesks', methods=["POST"])
def getAvailableDesks():
    if validateSession(connection, request.get_json()["token"]):
        return objectArrayToJson(selectUtils.getAvailableDesks(connection, request.get_json()["date"]))
    else:
        return "Session has expired or does not exist", 401


# login/usermanagement
@app.route('/login', methods=["POST"])
def login():
    requestJson = request.get_json()
    user = selectUtils.getUsers(connection, requestJson["email"])[0]
    if user.passwordHash == requestJson["passwordHash"]:
        session = secrets.token_urlsafe(16)
        insertInto(connection, Session(
            session, requestJson["email"], datetime.now() + timedelta(hours=8)))
        return session, 200
    return "Unable to authenticate", 400


@app.route('/register', methods=["POST"])
def register():
    requestJson = request.get_json()
    if len(getUsers(connection, requestJson["email"])) < 1:
        newUser = User(
            requestJson["email"], requestJson["name"], False, requestJson["passwordHash"])
        insertInto(connection, newUser)
        return "User added", 200
    return "User already exists", 400


@app.route('/registerAdmin', methods=["POST"])
def registerAdmin():
    requestJson = request.get_json()
    if validateSession(connection, requestJson["token"]):
        if getSessionUser(connection, requestJson["token"])[0].isAdmin == 'True':
            if len(getUsers(connection, requestJson["email"])) < 1:
                newUser = newUser = User(
                    requestJson["email"], requestJson["name"], True, requestJson["passwordHash"])
                insertInto(connection, newUser)
                return "User added", 200
            return "User already exists", 400
        return "Permission denied", 400
    return "Session has exipred or does not exist", 401


@app.route('/updateUser', methods=["POST"])
def updateUser():
    requestJson = request.get_json()
    if validateSession(connection, requestJson["token"]):
        user = getSessionUser(connection, requestJson["token"])[0]
        email = user.email
        isAdmin = False
        if user.isAdmin == 'True':
            try:
                email = requestJson["email"]
                user = getUsers(connection, email)[0]
            except:
                pass
            try:
                isAdmin = requestJson["isAdmin"]
            except:
                isAdmin = user.isAdmin
        else:
            try:
                requestJson["email"]
                return "Permission denied1", 400
            except:
                pass
        try:
            name = requestJson["name"]
        except:
            print("oof")
            name = user.name
        try:
            passwordHash = requestJson["passwordHash"]
        except:
            passwordHash = user.passwordHash

        updateRecord(connection, User(email, name, isAdmin, passwordHash))
        return "updated", 200
    return "unable to validate", 400


@app.route("/adminLogin", methods=["POST"])
def adminLogin():
    requestJson = request.get_json()
    user = selectUtils.getUsers(connection, requestJson["email"])[0]
    if user.passwordHash == requestJson["passwordHash"]:
        if user.isAdmin == 'True':
            session = secrets.token_urlsafe(16)
            insertInto(connection, Session(
            session, requestJson["email"], datetime.now() + timedelta(hours=8)))
            return session, 200
        else:
            return "User is not admin", 401

    return "Unable to authenticate", 401


app.run()
