from db import db

class TipAutoturism(db.Model):
    __tablename__ = 'tipautoturisme'

    codTipAutoturisme = db.Column(db.Integer, primary_key=True)
    denumireTipAutoturisme = db.Column(db.String(50), nullable=False)

    def __init__(self, denumireTipAutoturisme):
        self.denumireTipAutoturisme = denumireTipAutoturisme

    @property
    def serialize(self):
        return {
            'codTipAutoturisme': self.codTipAutoturisme,
            'denumireTipAutoturisme': self.denumireTipAutoturisme,
        }
