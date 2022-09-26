class Booking:
    bookingId = None
    deskId = None
    email = ""
    date = ""

    def __init__(self, bookingId, email, deskId, date):
        self.bookingId = bookingId
        self.deskId = deskId
        self.email = email
        self.date = date
