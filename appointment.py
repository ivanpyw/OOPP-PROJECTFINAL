class Appointment:
    def __init__(self, date, timee):
        self.date = date
        self.timee = timee
        self.pubid = ""

    def get_date(self):
        return self.date

    def get_timee(self):
        return self.timee

    def get_pubid(self):
        return self.pubid

    def set_date(self, date):
        self.date = date

    def set_timee(self, timee):
        self.timee = timee

    def set_pubid(self, pubid):
        self.pubid = pubid

