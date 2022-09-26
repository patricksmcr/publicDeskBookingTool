import sqlite3
from sqlite3 import Error
from datetime import datetime


def createConnection(path):
    connection = None
    try:
        connection = sqlite3.connect(path, check_same_thread=False)
        print(sqlite3.version)
    except Error as e:
        print(e)
    return connection


def insertInto(connection, record):
    sqlCommand = "INSERT INTO {table} ({fields}) VALUES ({values});"
    if type(record).__name__ == "User":
        sqlCommand = sqlCommand.format(
            table="user",
            fields="Email, Name, IsAdmin, PasswordHash",
            values=("'{}','{}','{}','{}'".format(record.email, record.name, record.isAdmin, record.passwordHash)))
        executeSqlCommand(connection, sqlCommand)

    elif type(record).__name__ == "Desk":
        if record.deskId == None:
            deskId = 'NULL'
        else:
            deskId = record.deskId
        sqlCommand = sqlCommand.format(
            table="desk",
            fields="DeskId, Room",
            values=("{},{}".format(deskId, record.room)))
        executeSqlCommand(connection, sqlCommand)

    elif type(record).__name__ == "Booking":
        if record.bookingId == None:
            bookingId = 'NULL'
        else:
            bookingId = record.bookingId
        sqlCommand = sqlCommand.format(
            table="booking",
            fields="BookingId, Email, DeskId, Date",
            values=("{},'{}',{},'{}'".format(bookingId, record.email, record.deskId, record.date)))
        executeSqlCommand(connection, sqlCommand)
    
    elif type(record).__name__ == "Session":
        sqlCommand = sqlCommand.format(
            table="Session",
            fields="Token, Email, ExpireTime",
            values=("'{}','{}','{}'".format(record.token, record.email, record.expireTime)))
        executeSqlCommand(connection, sqlCommand)


def selectFrom(connection, table, condition, fields="*"):
    sqlCommand = "SELECT {} FROM {} WHERE {};".format(
        fields, table.__name__, condition)
    response = []
    for record in executeSqlCommand(connection, sqlCommand):
        response.append(table(*record))
    return response


def deleteFrom(connection, table, condition):
    sqlCommand = "DELETE FROM {} WHERE {};".format(table.__name__, condition)
    return executeSqlCommand(connection, sqlCommand)

def updateRecord(connection, record):
    sqlCommand = "UPDATE {} SET {} WHERE {};"

    if type(record).__name__ == "User":
        sqlCommand = sqlCommand.format(
            "User",
            "Name='{}', IsAdmin='{}', PasswordHash='{}'".format(record.name, record.isAdmin, record.passwordHash),
            "Email='{}'".format(record.email)
        )
        executeSqlCommand(connection, sqlCommand)

    elif type(record).__name__ == "Booking":
        sqlCommand = sqlCommand.format(
            "Booking",
            "Email='{}', DeskId={}, Date='{}'".format(record.email, record.deskId, record.date),
            "BookingId='{}'".format(record.bookingId)
        )
        executeSqlCommand(connection, sqlCommand)
    
    elif type(record).__name__ == "Desk":
        sqlCommand = sqlCommand.format(
            "Desk",
            "Room='{}'".format(record.room),
            "DeskId='{}'".format(record.deskId)
        )
        executeSqlCommand(connection, sqlCommand)
    
    elif type(record).__name__ == "Session":
        sqlCommand = sqlCommand.format(
            "Session",
            "Email='{}', ExpireTime='{}'".format(record.email, record.expireTime),
            "Token='{}'".format(record.token)
        )
        executeSqlCommand(connection, sqlCommand)


def executeSqlCommand(connection, sql):
    try:
        print(datetime.now(), sql)
        cursor = connection.cursor()
        cursor.execute(sql)

        response = cursor.fetchall()
        print(datetime.now(), response)
        connection.commit()
        return response
    except Error as e:
        print(e)
