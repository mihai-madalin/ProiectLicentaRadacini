from db import db

class Dotare(db.Model):
    __tablename__ = 'dotari'

    codDotare = db.Column(db.Integer, primary_key=True)
    denumireDotare = db.Column(db.String(300), nullable=False)

    def __init__(self, denumireDotare):
        self.denumireDotare = denumireDotare

    @property
    def serialize(self):
        return {
            'codDotare': self.codDotare,
            'denumireDotare': self.denumireDotare,
        }
