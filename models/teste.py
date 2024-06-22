from db import db

class Test(db.Model):
    __tablename__ = 'teste'

    codTest = db.Column(db.Integer, primary_key=True)
    DenumireTest = db.Column(db.String(255), nullable=False)

    def __init__(self, DenumireTest):
        self.DenumireTest = DenumireTest

    @property
    def serialize(self):
        return {
            'codTest': self.codTeste,
            'DenumireTest': self.DenumireTest
        }
