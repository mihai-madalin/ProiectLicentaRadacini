from db import db

class TotalTeste(db.Model):
    __tablename__ = 'totalteste'

    codTotalTest = db.Column(db.Integer, primary_key=True)
    codCategorieTest = db.Column(db.Integer, db.ForeignKey('categorieteste.codCategorieTeste'), nullable=False)
    codTest = db.Column(db.Integer, db.ForeignKey('teste.codTest'), nullable=False)

    def __init__(self, codCategorieTest, codTest):
        self.codCategorieTest = codCategorieTest
        self.codTest = codTest

    @property
    def serialize(self):
        return {
            'codTotalTest': self.codTotalTest,
            'codCategorieTest': self.codCategorieTest,
            'codTest': self.codTest,
        }
