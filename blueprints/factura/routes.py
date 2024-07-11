from datetime import date
import os
from flask import Flask, render_template, request, redirect, send_file, url_for
from flask_login import current_user, login_required
from db import db
from models.autoturism import Autoturism
from models.client_persoana_juridica import ClientPersoanaJuridica
from models.ofertevanzare import OfertaVanzare
from . import facturi_bp
from models.facturafiscala import FacturaFiscala 
from models.componentefactura import ComponenteFactura
import pdfkit
from num2words import num2words
from sqlalchemy import func

SERIE_FACTURA = "VANZARI"

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
        facturi = FacturaFiscala.query.all()


        # Crează factura
        factura = FacturaFiscala(
            NumarFactura= (len(facturi) + 1),
            SerieFactura=SERIE_FACTURA,
            ResponsabilIntocmire=current_user.codUtilizator,
            # SETEAZA VALOAREA CTOR cu VALOAREA EXTRASA IN VAR codClientPersoanaJuridica
            codCumparatorPersoanaJuridica=codClientPersoanaJuridica,
            DataFacturi= date.today()
        )
        db.session.add(factura)
        db.session.commit()


        autoturism = Autoturism.query.get_or_404(request.form['codAutoturism'])
        

        componenta = ComponenteFactura(
                NumarFactura=factura.NumarFactura,
                SerieFactura=factura.SerieFactura,
                codInternContract=1,
                DenumireArticol=f'Autoturism {autoturism.marca} {autoturism.model} - An  {autoturism.AnulFabricatiei}  - {autoturism.valoareOdometru}',
                Cantiate=1,
                PretUnitar=request.form['valoareaContractului']
                )
        db.session.add(componenta)

        db.session.commit()

        return redirect(url_for('factura_bp.listaFacturi'))

    return render_template('factura/create_factura.html', autoturisme = autoturisme, clienti_persoane_juridice = pj, oferte=oferte )

@facturi_bp.route('/generate_factura/<int:codInternFactura>', methods=['GET'])
@login_required
def generate_facturi(codInternFactura):
    factura = FacturaFiscala.query.first_or_404([codInternFactura, SERIE_FACTURA])
    client = ClientPersoanaJuridica.query.get_or_404(factura.codCumparatorPersoanaJuridica)

    elementeFactura = ComponenteFactura.query.where(ComponenteFactura.NumarFactura == codInternFactura)

    rendered_html = render_template(
        'factura/factura.html',
        FacturaFiscala=factura,
        logo_url=url_for('static', filename='images/logo.jpg', _external=True) ,
        client = client,
        elementeFactura = elementeFactura,
        # valInNumere= num2words(factura.valoareaContractului, lang='ro')
        )

    directory = 'C:\\Facturi'
    if not os.path.exists(directory):
        os.makedirs(directory)

    pdf_file = pdfkit.from_string(rendered_html, False)

    pdf_path = os.path.join(directory, f'FF-{SERIE_FACTURA}-{codInternFactura}.pdf')
    with open(pdf_path, 'wb') as f:
        f.write(pdf_file)

    return send_file(pdf_path, as_attachment=True)


@facturi_bp.route('/', methods=["GET"])
@login_required
def listaFacturi():
    facturi = FacturaFiscala.query.all()
    return render_template('factura/list_factura.html', facturi=facturi)
