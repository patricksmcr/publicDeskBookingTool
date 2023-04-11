from src.utils.databaseUtils import createConnection, insertInto, deleteFrom, updateRecord
from src.utils.selectUtils import getUsers, getAllUsers
from src.models import User
connection = createConnection("src/resources/database.db")

import src.utils.dbCreation # noqa


def test_insertSingleRecord():
    user = User("testemail@email.com", "test name", "False", "hash")
    insertInto(connection, user)
    assert len(getUsers(connection, "testemail@email.com")) == 1


def test_insertExistingRecordShouldNotUpdate():
    user = User("user1@email.com", "testName", "False", "hash")
    insertInto(connection, user)
    assert getUsers(connection, "user1@email.com")[0].name == 'person 1'


def test_deleteSingleRecord():
    deleteFrom(connection, User, "email='testemail@email.com'")
    assert len(getUsers(connection, "testemail@email.com")) == 0


def test_deleteNonExistingRecord():
    deleteFrom(connection, User, "email='testemail@email.com'")
    assert len(getAllUsers(connection)) == 6


def test_updateRecord():
    user = User("user1@email.com", "test name", "False", "hash")
    updateRecord(connection, user)
    user = getUsers(connection, "user1@email.com")[0]
    assert user.name == "test name"


def test_updateRecordNonExistant():
    user = User("testuser@email.com", "test name", "False", "hash")
    updateRecord(connection, user)
    user = getUsers(connection, "testuser@email.com")
    assert len(user) == 0
