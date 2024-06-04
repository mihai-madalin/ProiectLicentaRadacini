from db import db

class FacturaFiscala(db.Model):
    __tablename__ = 'facturafiscala'

    NumarFactura = db.Column(db.Integer, primary_key=True)
    SerieFactura = db.Column(db.Integer, primary_key=True)
    ResponsabilIntocmire = db.Column(db.Integer, db.ForeignKey('utilizatori.codUtilizator'))
    codClientPersoanaJuridica = db.Column(db.Date, nullable=False)
    DataFacturi = db.Column(db.Date, nullable=False)

    def __init__(self, NumarFactura, SerieFactura, ResponsabilIntocmire, codClientPersoanaJuridica, DataFacturi):
        self.NumarFactura = NumarFactura
        self.SerieFactura = SerieFactura
        self.ResponsabilIntocmire = ResponsabilIntocmire
        self.codClientPersoanaJuridica = codClientPersoanaJuridica
        self.DataFacturi = DataFacturi

    @property
    def serialize(self):
        return {
            'NumarFactura': self.NumarFactura,
            'SerieFactura': self.SerieFactura,
            'ResponsabilIntocmire': self.ResponsabilIntocmire,
            'codClientPersoanaJuridica': self.codClientPersoanaJuridica,
            'DataFacturi': self.DataFacturi,
        }
