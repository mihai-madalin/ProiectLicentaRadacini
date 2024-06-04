from db import db

class Programare(db.Model):
    __tablename__ = 'programari'

    codProgramare = db.Column(db.Integer, primary_key=True)
    tipProgramre = db.Column(db.Integer, nullable=False)
    dataProgramare = db.Column(db.DateTime, nullable=False)
    codAutoturism = db.Column(db.Integer, db.ForeignKey('autototurisme.codAutoturism'))
    statusProgramre = db.Column(db.Integer)
    codClientPersoanaFizica = db.Column(db.Integer, db.ForeignKey('clientipersoanefizice.codClientPF'))
    codClientPersoanaJuridica = db.Column(db.Integer, db.ForeignKey('clientipersoanejuridice.codClientPJ'))
    codResponsabilIntocmire = db.Column(db.Integer, db.ForeignKey('utilizatori.codUtilizator'), nullable=False)

    def __init__(self, tipProgramre, dataProgramare, codAutoturism, statusProgramre, codClientPersoanaFizica, codClientPersoanaJuridica, codResponsabilIntocmire):
        self.tipProgramre = tipProgramre
        self.dataProgramare = dataProgramare
        self.codAutoturism = codAutoturism
        self.statusProgramre = statusProgramre
        self.codClientPersoanaFizica = codClientPersoanaFizica
        self.codClientPersoanaJuridica = codClientPersoanaJuridica
        self.codResponsabilIntocmire = codResponsabilIntocmire

    @property
    def serialize(self):
        return {
            'codProgramare': self.codProgramare,
            'tipProgramre': self.tipProgramre,
            'dataProgramare': self.dataProgramare,
            'codAutoturism': self.codAutoturism,
            'statusProgramre': self.statusProgramre,
            'codClientPersoanaFizica': self.codClientPersoanaFizica,
            'codClientPersoanaJuridica': self.codClientPersoanaJuridica,
            'codResponsabilIntocmire': self.codResponsabilIntocmire,
        }
