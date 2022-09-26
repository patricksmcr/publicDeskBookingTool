class User:
    email = ""
    name = ""
    isAdmin = False
    passwordHash = ""
    def __init__ (self, email, name, isAdmin, passwordHash):
        self.email = email
        self.name = name
        self.isAdmin = isAdmin
        self.passwordHash = passwordHash