import datetime
from email_validator import validate_email
from src.utils.selectUtils import getSession


def validateInputs(record):
    errors = []
    for key, value in record.items():
        if key in ["name", "token", "passwordHash"]:
            try:
                if "'" in value:
                    errors.append("Values cannot contain a ' character")
            except Exception:
                errors.append("Error with field"+key+"")
            
        if key in ["deskId", "bookingId"]:
            try:
                int(value)
            except Exception:
                errors.append(""+key+" must be an integer")

        if "date" == key:
            validDate = dateValidator(record["date"])
            if False in validDate.keys():
                errors.append(validDate[False])
            else:
                record["date"] = validDate[True]

        if "email" == key:
            isEmailValid = emailValidator(record["email"])
            if False in isEmailValid.keys():
                errors.append(isEmailValid[False])

        if "isAdmin" == key:
            isAdminValid = isAdminValidator(record["isAdmin"])
            if False in isAdminValid.keys():
                errors.append(isAdminValid[False])
    return errors


def validateSession(connection, token):
    if len(getSession(connection, token)) > 0:
        return True
    return False


def dateValidator(date):
    try:
        validDate = datetime.datetime.strptime(date, "%d/%m/%Y")
        validDate = validDate.strftime("%Y-%m-%d")
        return {True: validDate}
    except Exception:
        return {False: "Invalid date"}


def emailValidator(email):
    try:
        validate_email(email).email
        return {True: ""}
    except Exception:
        return {False: "Invalid email adress"}


def isAdminValidator(isAdmin):
    if isAdmin in ['True', 'False']:
        return {True: ''}
    else:
        return {False: "Field 'isAdmin' must be True or False"}
