import datetime
from email_validator import validate_email


def validateInputs(record):
    errors = []
    if "date" in record.keys():
        validDate = dateValidator(record["date"])
        if False in validDate.keys():
            errors.append(validDate[False])
        else:
            record["date"] = validDate[True]
        
    if "email" in record.keys():
        isEmailValid = emailValidator(record["email"])
        if False in isEmailValid.keys():
            errors.append(isEmailValid[False])

    if "isAdmin" in record.keys():
        isAdminValid = isAdminValidator(record["isAdmin"])
        if False in isAdminValid.keys():
            errors.append(isAdminValid[False])
    return errors


def dateValidator(date):
    try:
        validDate = datetime.datetime.strptime(date, "%d/%m/%Y")
        validDate = validDate.strftime("%Y-%m-%d")
        return {True: validDate}
    except Exception as e:
        return {False: "Invalid date"}


def emailValidator(email):
    try:
        validate_email(email).email
        return {True:""}
    except Exception as e:
        return {False: "Invalid email adress"}

def isAdminValidator(isAdmin):
    if isAdmin in ['True','False']:
        return {True:''}
    else:
        return{False:"Field 'isAdmin' must be True or False"}