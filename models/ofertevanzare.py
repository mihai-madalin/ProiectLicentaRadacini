from app import db

class OfertaVanzare(db.Model):
    __tablename__ = 'ofertevanzare'

    codOferta = db.Column(db.Integer, primary_key=True)
    tipOferta = db.Column(db.Integer, nullable=False)
    codAutorism = db.Column(db.Integer, db.ForeignKey('autototurisme.codAutoturism'), nullable=False)
    valoareOdometru = db.Column(db.Integer, nullable=False)
    pret = db.Column(db.Float, nullable=False)
    codInspectieTehnica = db.Column(db.Integer, db.ForeignKey('inspectii.codInspectie'), nullable=False)

    def __init__(self, tipOferta, codAutorism, valoareOdometru, pret, codInspectieTehnica):
        self.tipOferta = tipOferta
        self.codAutorism = codAutorism
        self.valoareOdometru = valoareOdometru
        self.pret = pret
        self.codInspectieTehnica = codInspectieTehnica

    @property
    def serialize(self):
        return {
            'codOferta': self.codOferta,
            'tipOferta': self.tipOferta,
            'codAutorism': self.codAutorism,
            'valoareOdometru': self.valoareOdometru,
            'pret': self.pret,
            'codInspectieTehnica': self.codInspectieTehnica,
        }
