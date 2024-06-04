from db import db

class Utilizator(db.Model):
    __tablename__ = 'utilizatori'

    codUtilizator = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), nullable=False)
    parola = db.Column(db.String(128), nullable=False)
    rol = db.Column(db.Integer, nullable=False)
    nume = db.Column(db.String(50), nullable=False)
    prenume = db.Column(db.String(50), nullable=False)
    serieActIdentitate = db.Column(db.String(2))
    numarActIdentate = db.Column(db.String(10), nullable=False)
    reseteazaParola = db.Column(db.Boolean, nullable=False)

    def __init__(self, email, parola, rol, nume, prenume, serieActIdentitate, numarActIdentate, reseteazaParola):
        self.email = email
        self.parola = parola
        self.rol = rol
        self.nume = nume
        self.prenume = prenume
        self.serieActIdentitate = serieActIdentitate
        self.numarActIdentate = numarActIdentate
        self.reseteazaParola = reseteazaParola

    @property
    def serialize(self):
        return {
            'codUtilizator': self.codUtilizator,
            'email': self.email,
            'parola': self.parola,
            'rol': self.rol,
            'nume': self.nume,
            'prenume': self.prenume,
            'serieActIdentitate': self.serieActIdentitate,
            'numarActIdentate': self.numarActIdentate,
            'reseteazaParola': self.reseteazaParola,
        }
