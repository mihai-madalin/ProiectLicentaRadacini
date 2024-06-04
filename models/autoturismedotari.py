from db import db

class AutoturismDotari(db.Model):
    __tablename__ = 'autoturismedotari'

    codAutoturismDotari = db.Column(db.Integer, primary_key=True)
    codAutoturism = db.Column(db.Integer, db.ForeignKey('autototurisme.codAutoturism'), nullable=False)
    codDotare = db.Column(db.Integer, db.ForeignKey('dotari.codDotare'), nullable=False)

    autoturism = db.relationship('Autototurism', backref=db.backref('dotari', lazy=True))
    dotare = db.relationship('Dotare', backref=db.backref('autoturisme', lazy=True))

    def __init__(self, codAutoturism, codDotare):
        self.codAutoturism = codAutoturism
        self.codDotare = codDotare

    @property
    def serialize(self):
        return {
            'codAutoturismDotari': self.codAutoturismDotari,
            'codAutoturism': self.codAutoturism,
            'codDotare': self.codDotare,
        }
