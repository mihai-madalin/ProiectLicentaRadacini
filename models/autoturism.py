from db import db

class Autoturism(db.Model):
    __tablename__ = 'autototurisme'

    codAutoturism = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    valoareOdometru = db.Column(db.Integer, nullable=False)
    tipAutoturism = db.Column(db.Integer, db.ForeignKey('tipautoturisme.codTipAutoturisme'), nullable=False)
    AnulFabricatiei = db.Column(db.Integer, nullable=False)
    serieCaroserie = db.Column(db.String(13), nullable=False)
    numarInmatriculare = db.Column(db.String(10), nullable=False)
    culoare = db.Column(db.String(50), nullable=False)
    dataPrimeiImatirculari = db.Column(db.Date, nullable=False)
    capacitateCilindrica = db.Column(db.Integer, nullable=False)
    combustibil = db.Column(db.Integer, nullable=False)
    numarPropietariAnteriori = db.Column(db.Integer, nullable=False)
    capacitateRezervorTermic = db.Column(db.Integer, nullable=True)
    capacitateAutonomieBaterie = db.Column(db.Integer, nullable=True)
    putereMotor = db.Column(db.Integer, nullable=False)
    tipTransmisie = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    
    
    # tipAutoturism = db.relationship('TipAutoturisme', backref=db.backref('tipautoturisme', lazy=True))
    # inspectie = db.relationship('Inspectie', backref=db.backref('ofertevanzare', lazy=True))

    
    
    def __init__(self, marca, model, valoareOdometru, tipAutoturism, AnulFabricatiei, serieCaroserie, numarInmatriculare, culoare, dataPrimeiImatirculari, capacitateCilindrica, combustibil, numarPropietariAnteriori, capacitateRezervorTermic, capacitateAutonomieBaterie, putereMotor, tipTransmisie, status):
        self.marca = marca
        self.model = model
        self.valoareOdometru = valoareOdometru
        self.tipAutoturism = tipAutoturism
        self.AnulFabricatiei = AnulFabricatiei
        self.serieCaroserie = serieCaroserie
        self.numarInmatriculare = numarInmatriculare
        self.culoare = culoare
        self.dataPrimeiImatirculari = dataPrimeiImatirculari
        self.capacitateCilindrica = capacitateCilindrica
        self.combustibil = combustibil
        self.numarPropietariAnteriori = numarPropietariAnteriori
        self.capacitateRezervorTermic = capacitateRezervorTermic
        self.capacitateAutonomieBaterie = capacitateAutonomieBaterie
        self.putereMotor = putereMotor
        self.tipTransmisie = tipTransmisie
        self.status = status
