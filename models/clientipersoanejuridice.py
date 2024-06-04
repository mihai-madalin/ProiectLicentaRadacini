from db import db

class ClientPersoanaJuridica(db.Model):
    __tablename__ = 'clientipersoanejuridice'

    codClientPJ = db.Column(db.Integer, primary_key=True)
    Nume = db.Column(db.String(255), nullable=False)
    NumarRegistrulComertului = db.Column(db.String(255))
    CUI = db.Column(db.String(255), nullable=False)
    SucursalaBancii = db.Column(db.String(255), nullable=False)
    IBAN = db.Column(db.String(255), nullable=False)
    Tara = db.Column(db.String(255), nullable=False)
    Judet = db.Column(db.String(255))
    Oras = db.Column(db.String(255), nullable=False)
    Strada = db.Column(db.String(255), nullable=False)
    Numar = db.Column(db.String(255), nullable=False)
    Scara = db.Column(db.String(255))
    Bloc = db.Column(db.String(255))
    Etaj = db.Column(db.String(255))
    Apartament = db.Column(db.String(255))
    numeReprezentant = db.Column(db.String(50), nullable=False)
    prenumeReprezentant = db.Column(db.String(50), nullable=False)
    telefonReprezentant = db.Column(db.String(10), nullable=False)
    CNPReprezentant = db.Column(db.String(13), nullable=False)
    judetReprezentant = db.Column(db.String(50))
    orasReprezentant = db.Column(db.String(50))
    stradaReprezentant = db.Column(db.String(50))
    numarReprezentant = db.Column(db.String(5))
    blocReprezentant = db.Column(db.String(5))
    scaraReprezentant = db.Column(db.String(5))
    etajReprezentant = db.Column(db.String(3))
    appartamentReprezentant = db.Column(db.String(4))

    def __init__(self, Nume, NumarRegistrulComertului, CUI, SucursalaBancii, IBAN, Tara, Judet, Oras, Strada, Numar, Scara, Bloc, Etaj, Apartament, numeReprezentant, prenumeReprezentant, telefonReprezentant, CNPReprezentant, judetReprezentant, orasReprezentant, stradaReprezentant, numarReprezentant, blocReprezentant, scaraReprezentant, etajReprezentant, appartamentReprezentant):
        self.Nume = Nume
        self.NumarRegistrulComertului = NumarRegistrulComertului
        self.CUI = CUI
        self.SucursalaBancii = SucursalaBancii
        self.IBAN = IBAN
        self.Tara = Tara
        self.Judet = Judet
        self.Oras = Oras
        self.Strada = Strada
        self.Numar = Numar
        self.Scara = Scara
        self.Bloc = Bloc
        self.Etaj = Etaj
        self.Apartament = Apartament
        self.numeReprezentant = numeReprezentant
        self.prenumeReprezentant = prenumeReprezentant
        self.telefonReprezentant = telefonReprezentant
        self.CNPReprezentant = CNPReprezentant
        self.judetReprezentant = judetReprezentant
        self.orasReprezentant = orasReprezentant
        self.stradaReprezentant = stradaReprezentant
        self.numarReprezentant = numarReprezentant
        self.blocReprezentant = blocReprezentant
        self.scaraReprezentant = scaraReprezentant
        self.etajReprezentant = etajReprezentant
        self.appartamentReprezentant = appartamentReprezentant

    @property
    def serialize(self):
        return {
            'codClientPJ': self.codClientPJ,
            'Nume': self.Nume,
            'NumarRegistrulComertului': self.NumarRegistrulComertului,
            'CUI': self.CUI,
            'SucursalaBancii': self.SucursalaBancii,
            'IBAN': self.IBAN,
            'Tara': self.Tara,
            'Judet': self.Judet,
            'Oras': self.Oras,
            'Strada': self.Strada,
            'Numar': self.Numar,
            'Scara': self.Scara,
            'Bloc': self.Bloc,
            'Etaj': self.Etaj,
            'Apartament': self.Apartament,
            'numeReprezentant': self.numeReprezentant,
            'prenumeReprezentant': self.prenumeReprezentant,
            'telefonReprezentant': self.telefonReprezentant,
            'CNPReprezentant': self.CNPReprezentant,
            'judetReprezentant': self.judetReprezentant,
            'orasReprezentant': self.orasReprezentant,
            'stradaReprezentant': self.stradaReprezentant,
            'numarReprezentant': self.numarReprezentant,
            'blocReprezentant': self.blocReprezentant,
            'scaraReprezentant': self.scaraReprezentant,
            'etajReprezentant': self.etajReprezentant,
            'appartamentReprezentant': self.appartamentReprezentant,
        }
