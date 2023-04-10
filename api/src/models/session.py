class Session:
    token = ""
    email = ""
    expireTime = None

    def __init__(self, token, email, expireTime):
        self.token = token
        self.email = email
        self.expireTime = expireTime
