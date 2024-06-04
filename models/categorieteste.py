from db import db

class CategorieTeste(db.Model):
    __tablename__ = 'categorieteste'

    codCategorieTeste = db.Column(db.Integer, primary_key=True)
    DenumireCategorieTeste = db.Column(db.String(255))

    def __init__(self, DenumireCategorieTeste):
        self.DenumireCategorieTeste = DenumireCategorieTeste

    @property
    def serialize(self):
        return {
            'codCategorieTeste': self.codCategorieTeste,
            'DenumireCategorieTeste': self.DenumireCategorieTeste,
        }
