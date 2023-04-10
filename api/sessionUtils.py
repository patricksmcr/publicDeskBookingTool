import sys
sys.path.append("../../")
from api.db.utils.selectUtils import getSession


def validateSession(connection, token):
    if len(getSession(connection, token)) > 0:
        return True
    return False
