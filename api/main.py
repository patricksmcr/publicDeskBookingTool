import sys
import pytest
from src.utils import createDb, populateDb, startSeessionSchedule
from application import startApp


def printHelperText():
    print('''The application can be ran without arguments. Below is a list of optional arguments:
    ***
    --dev, -d \t\t | Dev \t\t | Resets the db and populates it with dev data, then starts the API.
    --resetDev, -r \t | Restet Dev \t | Resets the db and populates it with dev data. Does not start the API.
    --clean, -c \t | Clean API \t | Resets the db, and starts the API. Does not populate the DB (an Admin login
\t\t\t\t\t ...will stillbe created).
    --test, -t \t\t | Runs tests \t | Resets the dev db and runs the unit tests. Does not start the API.
    ***
    ''')


if __name__ == "__main__":
    startSessionSchedule = True
    for i, arg in enumerate(sys.argv):
        if arg in ["--help", "-h"]:
            sys.exit(printHelperText())
        if arg in ["--resetDev", "-r"]:
            createDb()
            sys.exit(populateDb())
        if arg in ["--dev", "-d"]:
            createDb()
            populateDb()
        if arg in ["--clean", "-c"]:
            createDb()
        if arg in ["--test", "-t"]:
            createDb()
            populateDb()
            sys.exit(pytest.main(["tests"]))
        if arg in ["--remove-session-schedule", "-rss"]:
            stopSessionSchedule = False

    if startSessionSchedule:
        startSeessionSchedule()
    startApp()
