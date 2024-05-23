from app import db

class Inspectie(db.Model):
    __tablename__ = 'inspectii'

    codInspectie = db.Column(db.Integer, primary_key=True)
    codProgramre = db.Column(db.Integer, db.ForeignKey('programari.codProgramare'), nullable=False)
    NumarInmatriculare = db.Column(db.String(255), nullable=False)
    DataInspectiei = db.Column(db.DateTime, nullable=False)
    ValoareOdometru = db.Column(db.Integer, nullable=False)
    codResponsabilIntocmire = db.Column(db.Integer, db.ForeignKey('utilizatori.codUtilizator'), nullable=False)

    def __init__(self, codProgramre, NumarInmatriculare, DataInspectiei, ValoareOdometru, codResponsabilIntocmire):
        self.codProgramre = codProgramre
        self.NumarInmatriculare = NumarInmatriculare
        self.DataInspectiei = DataInspectiei
        self.ValoareOdometru = ValoareOdometru
        self.codResponsabilIntocmire = codResponsabilIntocmire

    @property
    def serialize(self):
        return {
            'codInspectie': self.codInspectie,
            'codProgramre': self.codProgramre,
            'NumarInmatriculare': self.NumarInmatriculare,
            'DataInspectiei': self.DataInspectiei,
            'ValoareOdometru': self.ValoareOdometru,
            'codResponsabilIntocmire': self.codResponsabilIntocmire,
        }
