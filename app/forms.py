from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String((100)))
    password = db.Column(db.String((100)))
    registerDate = db.Column(db.String((100)))
    totalProblems = db.Column(db.Integer)
    totalCorrect = db.Column(db.Integer)
    totalPercent = db.Column(db.Integer)
    theme = db.Column(db.String((10)))

    def __init__(self, username, password, registerDate):
        self.username = username
        self.password = password
        self.registerDate = registerDate
        self.totalProblems = 0
        self.totalCorrect = 0
        self.totalPercent = 0
        self.theme = "light"
