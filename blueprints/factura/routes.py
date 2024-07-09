from datetime import date
from flask import Flask, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from db import db
from models.autoturism import Autoturism
from models.client_persoana_juridica import ClientPersoanaJuridica
from models.ofertevanzare import OfertaVanzare
from . import facturi_bp
from models.facturafiscala import FacturaFiscala 
from models.componentefactura import ComponenteFactura


@facturi_bp.route('/create_factura', methods=['GET', 'POST'])
@login_required
def create_factura():
    # #TODO SCOATE LIMITA DE ROL 
    # if current_user.rol != 3:
    #     return redirect(url_for('homePage'))

    autoturisme = Autoturism.query.filter(Autoturism.status  >= 1).filter(Autoturism.status  <= 2).all()
    pj = ClientPersoanaJuridica.query.all()
    oferte =  list()
    # ABORDARE MANUALA

    for autoturism in autoturisme:
        tempOferte = OfertaVanzare.query.filter(OfertaVanzare.codAutorism == autoturism.codAutoturism).all()
        for of in tempOferte:
            oferte.append(of)


    if request.method == 'POST':
        # Extrage datele din formular

        # PREIA DIN FORMULARUL POST CAMPUL codClientPersoanaJuridica
        codClientPersoanaJuridica = request.form['codClientPersoanaJuridica']
        
        # Crează factura
        factura = FacturaFiscala(
            SerieFactura="VANZARI",
            ResponsabilIntocmire=current_user.codUtilizator,
            # SETEAZA VALOAREA CTOR cu VALOAREA EXTRASA IN VAR codClientPersoanaJuridica
            codCumparatorPersoanaJuridica=codClientPersoanaJuridica,
            DataFacturi= date.today()
        )
        db.session.add(factura)
        db.session.commit()

        # Extrage componentele
        codInternContract_list = request.form.getlist('codInternContract[]')
        DenumireArticol_list = request.form.getlist('DenumireArticol[]')
        Cantiate_list = request.form.getlist('Cantiate[]')
        PretUnitar_list = request.form.getlist('PretUnitar[]')

        for i in range(len(codInternContract_list)):
            componenta = ComponenteFactura(
                NumarFactura=NumarFactura,
                SerieFactura=SerieFactura,
                codInternContract=codInternContract_list[i],
                DenumireArticol=DenumireArticol_list[i],
                Cantiate=Cantiate_list[i],
                PretUnitar=PretUnitar_list[i]
            )
            db.session.add(componenta)

        db.session.commit()

        return redirect(url_for('homePage'))

    return render_template('factura/create_factura.html', autoturisme = autoturisme, clienti_persoane_juridice = pj, oferte=oferte )
