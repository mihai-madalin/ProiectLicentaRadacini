from app import db

class ClientPersoanaFizica(db.Model):
    __tablename__ = 'clientipersoanefizice'

    codClientPF = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(50), nullable=False)
    prenume = db.Column(db.String(50), nullable=False)
    telefon = db.Column(db.String(10), nullable=False)
    CNP = db.Column(db.String(13))
    judet = db.Column(db.String(50))
    oras = db.Column(db.String(50))
    strada = db.Column(db.String(50))
    numar = db.Column(db.String(5))
    bloc = db.Column(db.String(5))
    scara = db.Column(db.String(5))
    etaj = db.Column(db.String(3))
    appartament = db.Column(db.String(4))

    def __init__(self, nume, prenume, telefon, CNP, judet, oras, strada, numar, bloc, scara, etaj, appartament):
        self.nume = nume
        self.prenume = prenume
        self.telefon = telefon
        self.CNP = CNP
        self.judet = judet
        self.oras = oras
        self.strada = strada
        self.numar = numar
        self.bloc = bloc
        self.scara = scara
        self.etaj = etaj
        self.appartament = appartament

    @property
    def serialize(self):
        return {
            'codClientPF': self.codClientPF,
            'nume': self.nume,
            'prenume': self.prenume,
            'telefon': self.telefon,
            'CNP': self.CNP,
            'judet': self.judet,
            'oras': self.oras,
            'strada': self.strada,
            'numar': self.numar,
            'bloc': self.bloc,
            'scara': self.scara,
            'etaj': self.etaj,
            'appartament': self.appartament,
        }
