from db import db
from sqlalchemy.orm import relationship, backref

class ContractVanzareCumparare(db.Model):
    __tablename__ = 'contractevanzarecumparare'

    codInternContract = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vandutDeRadacini = db.Column(db.Boolean, nullable=False)
    vanzatorPersoanaJuridica = db.Column(db.Boolean, nullable=False)
    cumparatorPersoanaJuridica = db.Column(db.Boolean, nullable=False)
    codAutoturism = db.Column(db.Integer, db.ForeignKey('autototurisme.codAutoturism'), nullable=False)
    codInternVanzatorPersoanaFizica = db.Column(db.Integer, db.ForeignKey('clientipersoanefizice.codClientPF'))
    codInternVanzatorPersoanaJuridica = db.Column(db.Integer, db.ForeignKey('clientipersoanejuridice.codClientPJ'))
    codInternCumparatorPersoanaFizica = db.Column(db.Integer, db.ForeignKey('clientipersoanefizice.codClientPF'))
    codInternCumparatorPersoanaJuridica = db.Column(db.Integer, db.ForeignKey('clientipersoanejuridice.codClientPJ'))
    codResoinsabilIntocmire = db.Column(db.Integer, db.ForeignKey('utilizatori.codUtilizator'), nullable=False)
    valoareaContractului = db.Column(db.Float, nullable=False)
    codOferta = db.Column(db.Integer, db.ForeignKey('ofertevanzare.codOferta'))

    autoturism = relationship('Autoturism', backref=backref('contracte', lazy='dynamic'))
    vanzatorPF = relationship('ClientPersoanaFizica', foreign_keys=[codInternVanzatorPersoanaFizica])
    vanzatorPJ = relationship('ClientPersoanaJuridica', foreign_keys=[codInternVanzatorPersoanaJuridica])
    cumparatorPF = relationship('ClientPersoanaFizica', foreign_keys=[codInternCumparatorPersoanaFizica])
    cumparatorPJ = relationship('ClientPersoanaJuridica', foreign_keys=[codInternCumparatorPersoanaJuridica])
    responsabil = relationship('Utilizator', foreign_keys=[codResoinsabilIntocmire])
    oferta = relationship('OfertaVanzare', foreign_keys=[codOferta])

    def __init__(self, vandutDeRadacini, vanzatorPersoanaJuridica, cumparatorPersoanaJuridica, codAutoturism,
                 codResoinsabilIntocmire, valoareaContractului, codOferta,
                 codInternVanzatorPersoanaFizica=None, codInternVanzatorPersoanaJuridica=None,
                 codInternCumparatorPersoanaFizica=None, codInternCumparatorPersoanaJuridica=None):
        self.vandutDeRadacini = vandutDeRadacini
        self.vanzatorPersoanaJuridica = vanzatorPersoanaJuridica
        self.cumparatorPersoanaJuridica = cumparatorPersoanaJuridica
        self.codAutoturism = codAutoturism
        self.codResoinsabilIntocmire = codResoinsabilIntocmire
        self.valoareaContractului = valoareaContractului
        self.codOferta = codOferta
        self.codInternVanzatorPersoanaFizica = codInternVanzatorPersoanaFizica
        self.codInternVanzatorPersoanaJuridica = codInternVanzatorPersoanaJuridica
        self.codInternCumparatorPersoanaFizica = codInternCumparatorPersoanaFizica
        self.codInternCumparatorPersoanaJuridica = codInternCumparatorPersoanaJuridica

    @property
    def serialize(self):
        return {
            'codInternContract': self.codInternContract,
            'vandutDeRadacini': self.vandutDeRadacini,
            'vanzatorPersoanaJuridica': self.vanzatorPersoanaJuridica,
            'cumparatorPersoanaJuridica': self.cumparatorPersoanaJuridica,
            'codAutoturism': self.codAutoturism,
            'codInternVanzatorPersoanaFizica': self.codInternVanzatorPersoanaFizica,
            'codInternVanzatorPersoanaJuridica': self.codInternVanzatorPersoanaJuridica,
            'codInternCumparatorPersoanaFizica': self.codInternCumparatorPersoanaFizica,
            'codInternCumparatorPersoanaJuridica': self.codInternCumparatorPersoanaJuridica,
            'codResoinsabilIntocmire': self.codResoinsabilIntocmire,
            'valoareaContractului': self.valoareaContractului,
            'codOferta': self.codOferta
        }
