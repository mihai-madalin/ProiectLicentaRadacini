from flask import render_template, request, redirect, send_file, url_for, flash

from models.autoturisme_dotari import AutoturismDotari
from models.autoturisme_fotografii import AutoturismFotografii
from models.dotari import Dotare
from models.programari import Programare
from . import oferte_vanzare_bp
from db import db
from models.ofertevanzare import OfertaVanzare
from models.autoturism import Autoturism
from models.inspectii import Inspectie
from flask_login import login_required
import pdfkit

TIP_TRANSMISIE = {
    1: 'Manuală',
    2: 'Automată',
}

STATUS = {
    0: 'Neverificată',
    1: 'Verificată',
    2: 'În curs de vânzare',
    3: 'Vândut',
    4: 'Retrasă',
}

COMBUSTIBIL = {
    1: 'Benzină',
    2: 'Motorină',
    3: 'Electric',
    4: 'Benzina + GPL',
    5: 'Diesel + GNC',
    6: 'Hibrid + Benzina',
    7: 'Hibrid + Diesel',
    9: 'Hidrogen',
}


@oferte_vanzare_bp.route('/', methods=['GET'])
@login_required
def list_oferte():
    oferte = OfertaVanzare.query.all()
    return render_template('ofertevanzare/list_oferte.html', oferte=oferte)

@oferte_vanzare_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_oferta():
    autoturisme = Autoturism.query.all()
    inspectii = Inspectie.query.all()

    if request.method == 'POST':
        tipOferta = request.form.get('tipOferta')
        codAutorism = request.form.get('codAutorism')
        valoareOdometru = request.form.get('valoareOdometru')
        pret = request.form.get('pret')
        codInspectieTehnica = request.form.get('codInspectieTehnica')

        new_oferta = OfertaVanzare(tipOferta, codAutorism, valoareOdometru, pret, codInspectieTehnica)
        db.session.add(new_oferta)
        db.session.commit()

        flash('Oferta a fost creată cu succes!', 'success')
        return redirect(url_for('oferte_vanzare.list_oferte'))

    return render_template('ofertevanzare/create_oferta.html', autoturisme=autoturisme, inspectii=inspectii)

@oferte_vanzare_bp.route('/<int:codOferta>/edit', methods=['GET', 'POST'])
@login_required
def edit_oferta(codOferta):
    oferta = OfertaVanzare.query.get_or_404(codOferta)
    autoturisme = Autoturism.query.all()
    inspectii = Inspectie.query.all()

    if request.method == 'POST':
        oferta.tipOferta = request.form.get('tipOferta')
        oferta.valoareOdometru = request.form.get('valoareOdometru')
        oferta.pret = request.form.get('pret')

        db.session.commit()
        flash('Oferta a fost actualizată cu succes!', 'success')
        return redirect(url_for('oferte_vanzare.list_oferte'))

    return render_template('ofertevanzare/edit_oferta.html', oferta=oferta, autoturisme=autoturisme, inspectii=inspectii)

@oferte_vanzare_bp.route('/<int:codOferta>/delete', methods=['POST'])
@login_required
def delete_oferta(codOferta):
    oferta = OfertaVanzare.query.get_or_404(codOferta)
    db.session.delete(oferta)
    db.session.commit()
    flash('Oferta a fost ștearsă cu succes!', 'success')
    return redirect(url_for('oferte_vanzare.list_oferte'))


@oferte_vanzare_bp.route('/generate/<int:codOferta>', methods=['GET'])
@login_required
def generate_offer_report(codOferta):
    oferta = OfertaVanzare.query.get_or_404(codOferta)
    autoturism = Autoturism.query.get_or_404(oferta.codAutorism)
    programari = Programare.query.filter_by(codAutoturism=oferta.codAutorism).all()
    inspectii = Inspectie.query.filter(Inspectie.codProgramre.in_([p.codProgramare for p in programari])).all()
    
    dotari = db.session.query(AutoturismDotari, Dotare).join(Dotare, AutoturismDotari.codDotare == Dotare.codDotare).filter(AutoturismDotari.codAutoturism == oferta.codAutorism).all()
    fotografii = AutoturismFotografii.query.filter_by(codAutoturism=oferta.codAutorism).all()
    oferte_anterioare = OfertaVanzare.query.filter_by(codAutorism=oferta.codAutorism).all()

    # Display values
    tip_transmisie = TIP_TRANSMISIE.get(autoturism.tipTransmisie, 'N/A')
    status = STATUS.get(autoturism.status, 'N/A')
    combustibil = COMBUSTIBIL.get(autoturism.combustibil, 'N/A')

    # Apply rules for electric cars
    if autoturism.combustibil == 3:
        autoturism.capacitateRezervorTermic = None
    elif autoturism.combustibil in [1, 2, 4, 5, 9]:
        autoturism.capacitateAutonomieBaterie = None

    rendered_html = render_template(
        'ofertevanzare/offer_report.html',
        oferta=oferta,
        autoturism=autoturism,
        inspectii=inspectii,
        dotari=[d[1].denumireDotare for d in dotari],
        fotografii=fotografii,
        oferte_anterioare=oferte_anterioare,
        tip_transmisie=tip_transmisie,
        status=status,
        combustibil=combustibil,
        logo_url=url_for('static', filename='images/logo.jpg', _external=True)  # Use absolute URL
    )

    pdf_file = pdfkit.from_string(rendered_html, False)

    pdf_path = f'C:\\Rapoarte\\offer_report_{codOferta}.pdf'
    with open(pdf_path, 'wb') as f:
        f.write(pdf_file)

    return send_file(pdf_path, as_attachment=True)