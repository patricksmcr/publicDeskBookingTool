from src.utils.databaseUtils import createConnection  # noqa
from src.utils.selectUtils import getUsers, getAllUsers, getAvailableDesks, getBooking, getDateBookings, getDeskBookings, getSession, getSessionUser, getUserBookings # noqa
from src.utils.validation import validateInputs, validateSession # noqa
import src.utils.dbCreation  # noqa


connection = createConnection("src/resources/database.db")


def test_validDatePasses():
    assert len(validateInputs({"date": "01/01/2000"})) == 0


def test_invalidDateFormatFails():
    assert len(validateInputs({"date": "2000/01/01"})) == 1


def test_invalidDateNumbersFails():
    assert len(validateInputs({"date": "31/02/2000"})) == 1


def test_validEmailPasses():
    assert len(validateInputs({"email": "validemail@email.com"})) == 0


def test_invalidEmailFails():
    assert len(validateInputs({"email": "invalidemail@email@.com"})) == 1


def test_validDateAndEmailPasses():
    assert len(validateInputs({"date": "01/01/2000", "email": "invalidemail@email.com"})) == 0


def test_invalidDateAndEmailPasses():
    assert len(validateInputs({"date": "32/01/2000", "email": "invalid@email@email.com"})) == 2


def test_validStringField():
    assert len(validateInputs({"name": "Human Name"})) == 0


def test_invalidStringFieldContainsInvalidCharacter():
    assert len(validateInputs({"name": "Human's Name"})) == 1


def test_invalidStringFieldIsNotString():
    assert len(validateInputs({"name": 123})) == 1


def test_validIntegerInputIsString():
    assert len(validateInputs({"deskId": "123"})) == 0


def test_validIntegerInputIsInteger():
    assert len(validateInputs({"deskId": 123})) == 0


def test_invalidIntegerInputIsStringAndNotInteger():
    assert len(validateInputs({"deskId": "1.23"})) == 1


def test_validSession():
    assert validateSession(connection, "token1")


def test_invalidSession():
    assert validateSession(connection, "invalidToken") is False


