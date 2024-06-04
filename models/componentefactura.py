from db import db

class ComponenteFactura(db.Model):
    __tablename__ = 'componentefactura'

    codComponenteFactura = db.Column(db.Integer, primary_key=True)
    NumarFactura = db.Column(db.Integer, nullable=False)
    SerieFactura = db.Column(db.Integer, nullable=False)
    codInternContract = db.Column(db.Integer, db.ForeignKey('contractevanzarecumparare.codInternContract'))
    DenumireArticol = db.Column(db.String(255), nullable=False)
    Cantiate = db.Column(db.Integer, nullable=False)
    PretUnitar = db.Column(db.Float, nullable=False)

    def __init__(self, NumarFactura, SerieFactura, codInternContract, DenumireArticol, Cantiate, PretUnitar):
        self.NumarFactura = NumarFactura
        self.SerieFactura = SerieFactura
        self.codInternContract = codInternContract
        self.DenumireArticol = DenumireArticol
        self.Cantiate = Cantiate
        self.PretUnitar = PretUnitar

    @property
    def serialize(self):
        return {
            'codComponenteFactura': self.codComponenteFactura,
            'NumarFactura': self.NumarFactura,
            'SerieFactura': self.SerieFactura,
            'codInternContract': self.codInternContract,
            'DenumireArticol': self.DenumireArticol,
            'Cantiate': self.Cantiate,
            'PretUnitar': self.PretUnitar,
        }
