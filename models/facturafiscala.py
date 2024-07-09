from db import db

class FacturaFiscala(db.Model):
    __tablename__ = 'facturafiscala'

    NumarFactura = db.Column(db.Integer, primary_key=True)
    SerieFactura = db.Column(db.Integer, primary_key=True)
    ResponsabilIntocmire = db.Column(db.Integer, db.ForeignKey('utilizatori.codUtilizator'))
    codCumparatorPersoanaJuridica = db.Column(db.Integer, db.ForeignKey('clientipersoanejuridice.codClientPJ'))
    DataFacturi = db.Column(db.Date, nullable=False)

    def __init__(self, SerieFactura, ResponsabilIntocmire, DataFacturi, codCumparatorPersoanaJuridica):
        self.SerieFactura = SerieFactura
        self.ResponsabilIntocmire = ResponsabilIntocmire
        self.DataFacturi = DataFacturi
        self.codCumparatorPersoanaJuridica = codCumparatorPersoanaJuridica

    @property
    def serialize(self):
        return {
            'NumarFactura': self.NumarFactura,
            'SerieFactura': self.SerieFactura,
            'ResponsabilIntocmire': self.ResponsabilIntocmire,
            'codClientPersoanaJuridica': self.codClientPersoanaJuridica,
            'DataFacturi': self.DataFacturi,
        }
