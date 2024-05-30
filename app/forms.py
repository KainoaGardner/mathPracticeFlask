from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String((100)))
    password = db.Column(db.String((100)))
    registerDate = db.Column(db.String((100)))
    totalProblems = db.Column(db.Integer)
    totalCorrect = db.Column(db.Integer)

    def __init__(self, username, password, registerDate, totalProblems, totalCorrect):
        self.username = username
        self.password = password
        self.registerDate = registerDate
        self.totalProblems = totalProblems
        self.totalCorrect = totalCorrect
