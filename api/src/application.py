import secrets
from flask import Flask, request
from flask_cors import CORS
from src.utils.databaseUtils import createConnection, deleteFrom, insertInto, updateRecord
from src.utils import objectArrayToJson, validateInputs, validateSession
from src.utils import selectUtils
from src.models import Booking, Session, User
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

connection = createConnection("src/resources/database.db")


def startApp():
    app.run(ssl_context='adhoc')


@app.route('/getUserBookings', methods=["POST"])
def getUserBookings():
    requestJson = request.get_json()
    if validateSession(connection, requestJson["token"]):
        validationErrors = validateInputs(requestJson)
        if len(validationErrors) != 0:
            return ", ".join(validationErrors), 400
        return objectArrayToJson(selectUtils.getUserBookings(connection, request.get_json()["email"]))
    else:
        return "Session has expired or does not exist", 401


@app.route('/getDeskBookings', methods=["POST"])
def getDeskBookings():
    requestJson = request.get_json()
    if validateSession(connection, requestJson["token"]):
        validationErrors = validateInputs(requestJson)
        if len(validationErrors) != 0:
            return ", ".join(validationErrors), 400
        return objectArrayToJson(selectUtils.getDeskBookings(connection, request.get_json()["deskId"]))
    else:
        return "Session has expired or does not exist", 401


@app.route('/getDateBookings', methods=["POST"])
def getDateBookings():
    requestJson = request.get_json()
    if validateSession(connection, requestJson["token"]):
        validationErrors = validateInputs(requestJson)
        if len(validationErrors) != 0:
            return ", ".join(validationErrors), 400
        return objectArrayToJson(selectUtils.getDateBookings(connection, request.get_json()["date"]))
    else:
        return "Session has expired or does not exist", 401


@app.route('/createBooking', methods=["POST"])
def createBookings():
    requestJson = request.get_json()
    if validateSession(connection, requestJson["token"]):
        validationErrors = validateInputs(requestJson)
        if len(validationErrors) != 0:
            return ", ".join(validationErrors), 400
        availableDesks = selectUtils.getAvailableDesks(
            connection, requestJson["date"])
        email = selectUtils.getSessionUser(
            connection, request.get_json()["token"])[0].email
        for desk in availableDesks:
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
        admin = selectUtils.getSessionUser(
            connection, request.get_json()["token"])[0]
        if admin.isAdmin == 'False':
            return "Permission denied", 400
        validationErrors = validateInputs(requestJson)
        if len(validationErrors) != 0:
            return ", ".join(validationErrors), 400
        availableDesks = selectUtils.getAvailableDesks(
            connection, requestJson["date"])
        for desk in availableDesks:
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
        validationErrors = validateInputs(requestJson)
        if len(validationErrors) != 0:
            return ", ".join(validationErrors), 400
        booking = selectUtils.getBooking(connection, requestJson["bookingId"])
        if len(booking) == 0:
            return "Booking could not be found", 404
        user = selectUtils.getSessionUser(connection, requestJson["token"])[0]
        if booking[0].email == user.email:
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
    requestJson = request.get_json()
    if validateSession(connection, request.get_json()["token"]):
        validationErrors = validateInputs(requestJson)
        if len(validationErrors) != 0:
            return ", ".join(validationErrors), 400
        return objectArrayToJson(selectUtils.getAvailableDesks(connection, request.get_json()["date"]))
    else:
        return "Session has expired or does not exist", 401


# login/usermanagement
@app.route('/login', methods=["POST"])
def login():
    requestJson = request.get_json()
    validationErrors = validateInputs(requestJson)
    if len(validationErrors) != 0:
        return ", ".join(validationErrors), 400
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
    validationErrors = validateInputs(requestJson)
    if len(validationErrors) != 0:
        return ", ".join(validationErrors), 400
    if len(selectUtils.getUsers(connection, requestJson["email"])) < 1:
        newUser = User(
            requestJson["email"], requestJson["name"], False, requestJson["passwordHash"])
        insertInto(connection, newUser)
        return "User added", 200
    return "User already exists", 400


@app.route('/registerAdmin', methods=["POST"])
def registerAdmin():
    requestJson = request.get_json()
    if validateSession(connection, requestJson["token"]):
        validationErrors = validateInputs(requestJson)
        if len(validationErrors) != 0:
            return ", ".join(validationErrors), 400
        if selectUtils.getSessionUser(connection, requestJson["token"])[0].isAdmin == 'True':
            if len(selectUtils.getUsers(connection, requestJson["email"])) < 1:
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
        validationErrors = validateInputs(requestJson)
        if len(validationErrors) != 0:
            return ", ".join(validationErrors), 400
        requestingUser = selectUtils.getSessionUser(
            connection, requestJson["token"])[0]

        email = requestJson["email"]
        isAdmin = 'False'
        if requestingUser.isAdmin == 'True':
            try:
                user = selectUtils.getUsers(connection, email)[0]
            except Exception:
                return "User could not be found"
            try:
                isAdmin = requestJson["isAdmin"]
            except Exception:
                isAdmin = user.isAdmin
        else:
            try:
                if requestingUser.email != email:
                    return "Permission denied (HERE)", 400
                user = selectUtils.getUsers(connection, email)[0]
                if requestJson["isAdmin"] == 'True' and requestingUser.isAdmin == 'False':
                    return "Permission denied", 401
                isAdmin = user.isAdmin
            except Exception:
                return "Missing fields", 400
        try:
            name = requestJson["name"]
        except Exception:
            name = user.name
        try:
            passwordHash = requestJson["passwordHash"]
        except Exception:
            passwordHash = user.passwordHash

        updateRecord(connection, User(email, name, isAdmin, passwordHash))
        return "User updated", 200
    return "Session has exipred or does not exist", 401


@app.route("/adminLogin", methods=["POST"])
def adminLogin():
    requestJson = request.get_json()
    validationErrors = validateInputs(requestJson)
    if len(validationErrors) != 0:
        return ", ".join(validationErrors), 400
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
