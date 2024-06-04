from db import db

class ContractVanzareCumparare(db.Model):
    __tablename__ = 'contractevanzarecumparare'

    codInternContract = db.Column(db.Integer, primary_key=True)
    vandutDeRadacini = db.Column(db.Boolean)
    vanzatorPersoanaJuridica = db.Column(db.Boolean)
    cumparatorPersoanaJuridica = db.Column(db.Boolean)
    codAutoturism = db.Column(db.Integer, db.ForeignKey('autototurisme.codAutoturism'), nullable=False)
    codInternVanzatorPersoanaFizica = db.Column(db.Integer, db.ForeignKey('clientipersoanefizice.codClientPF'))
    codInternVanzatorPersoanaJuridica = db.Column(db.Integer, db.ForeignKey('clientipersoanejuridice.codClientPJ'))
    codInternCumparatorPersaonaFizica = db.Column(db.Integer, db.ForeignKey('clientipersoanefizice.codClientPF'))
    codInternCumparatorPersaonaJuridica = db.Column(db.Integer, db.ForeignKey('clientipersoanejuridice.codClientPJ'))
    codResoinsabilIntocmire = db.Column(db.Integer, db.ForeignKey('utilizatori.codUtilizator'), nullable=False)
    valoareaContractului = db.Column(db.Float, nullable=False)
    codOferta = db.Column(db.Integer, db.ForeignKey('ofertevanzare.codOferta'))

    def __init__(self, vandutDeRadacini, vanzatorPersoanaJuridica, cumparatorPersoanaJuridica, codAutoturism, codInternVanzatorPersoanaFizica, codInternVanzatorPersoanaJuridica, codInternCumparatorPersaonaFizica, codInternCumparatorPersaonaJuridica, codResoinsabilIntocmire, valoareaContractului, codOferta):
        self.vandutDeRadacini = vandutDeRadacini
        self.vanzatorPersoanaJuridica = vanzatorPersoanaJuridica
        self.cumparatorPersoanaJuridica = cumparatorPersoanaJuridica
        self.codAutoturism = codAutoturism
        self.codInternVanzatorPersoanaFizica = codInternVanzatorPersoanaFizica
        self.codInternVanzatorPersoanaJuridica = codInternVanzatorPersoanaJuridica
        self.codInternCumparatorPersaonaFizica = codInternCumparatorPersaonaFizica
        self.codInternCumparatorPersaonaJuridica = codInternCumparatorPersaonaJuridica
        self.codResoinsabilIntocmire = codResoinsabilIntocmire
        self.valoareaContractului = valoareaContractului
        self.codOferta = codOferta

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
            'codInternCumparatorPersaonaFizica': self.codInternCumparatorPersaonaFizica,
            'codInternCumparatorPersaonaJuridica': self.codInternCumparatorPersaonaJuridica,
            'codResoinsabilIntocmire': self.codResoinsabilIntocmire,
            'valoareaContractului': self.valoareaContractului,
            'codOferta': self.codOferta,
        }
