from db import db

class AutoturismFotografii(db.Model):
    __tablename__ = 'autoturismefotografii'

    codAutoturismFotografii = db.Column(db.Integer, primary_key=True)
    codAutoturism = db.Column(db.Integer, db.ForeignKey('autototurisme.codAutoturism'), nullable=False)
    caleDiscFotografie = db.Column(db.String(256), nullable=False)
    fotografiePrincipala = db.Column(db.Boolean, nullable=False)

    def __init__(self, codAutoturism, caleDiscFotografie, fotografiePrincipala):
        self.codAutoturism = codAutoturism
        self.caleDiscFotografie = caleDiscFotografie
        self.fotografiePrincipala = fotografiePrincipala

    @property
    def serialize(self):
        return {
            'codAutoturismFotografii': self.codAutoturismFotografii,
            'codAutoturism': self.codAutoturism,
            'caleDiscFotografie': self.caleDiscFotografie,
            'fotografiePrincipala': self.fotografiePrincipala,
        }
