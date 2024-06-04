from db import db

class Test(db.Model):
    __tablename__ = 'teste'

    codTeste = db.Column(db.Integer, primary_key=True)
    codCategorieTest = db.Column(db.Integer, db.ForeignKey('categorieteste.codCategorieTeste'))
    DenumireTest = db.Column(db.String(255), nullable=False)

    def __init__(self, codCategorieTest, DenumireTest):
        self.codCategorieTest = codCategorieTest
        self.DenumireTest = DenumireTest

    @property
    def serialize(self):
        return {
            'codTeste': self.codTeste,
            'codCategorieTest': self.codCategorieTest,
            'DenumireTest': self.DenumireTest,
        }
