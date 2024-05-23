from app import db

class InspectieTest(db.Model):
    __tablename__ = 'inspectiiteste'

    codInspectieTest = db.Column(db.Integer, primary_key=True)
    codInspectie = db.Column(db.Integer, db.ForeignKey('inspectii.codInspectie'), nullable=False)
    codTest = db.Column(db.Integer, db.ForeignKey('teste.codTeste'), nullable=False)
    rezultatTest = db.Column(db.Integer, nullable=False)
    DetaliiTest = db.Column(db.String(255))

    def __init__(self, codInspectie, codTest, rezultatTest, DetaliiTest):
        self.codInspectie = codInspectie
        self.codTest = codTest
        self.rezultatTest = rezultatTest
        self.DetaliiTest = DetaliiTest

    @property
    def serialize(self):
        return {
            'codInspectieTest': self.codInspectieTest,
            'codInspectie': self.codInspectie,
            'codTest': self.codTest,
            'rezultatTest': self.rezultatTest,
            'DetaliiTest': self.DetaliiTest,
        }
