from flask import render_template, request, redirect, send_file, url_for, flash, session
from . import contracts_bp
from db import db
from models.contractevanzarecumparare import ContractVanzareCumparare
from models.ofertevanzare import OfertaVanzare
from models.autoturism import Autoturism
from models.client_persoana_fizica import ClientPersoanaFizica
from models.client_persoana_juridica import ClientPersoanaJuridica
from models.utilizatori import Utilizator
from flask_login import login_required, current_user
import pdfkit
from num2words import num2words
import os

@contracts_bp.route('/', methods=['GET'])
@login_required
def list_contracts():
    contracts = ContractVanzareCumparare.query.all()
    return render_template('contracte/list_contracts.html', contracts=contracts)

@contracts_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_contract():
    if request.method == 'POST':
        vandutDeRadacini = request.form.get('vandutDeRadacini') == 'true'
        vanzatorPersoanaJuridica = request.form.get('vanzatorPersoanaJuridica') == 'true'
        cumparatorPersoanaJuridica = request.form.get('cumparatorPersoanaJuridica') == 'true'
        codAutoturism = request.form.get('codAutoturism')
        codInternVanzatorPersoanaFizica = request.form.get('codInternVanzatorPersoanaFizica') or None
        codInternVanzatorPersoanaJuridica = request.form.get('codInternVanzatorPersoanaJuridica') or None
        codInternCumparatorPersoanaFizica = request.form.get('codInternCumparatorPersoanaFizica') or None
        codInternCumparatorPersoanaJuridica = request.form.get('codInternCumparatorPersoanaJuridica') or None
        codResoinsabilIntocmire = current_user.codUtilizator
        valoareaContractului = request.form.get('valoareaContractului')
        codOferta = request.form.get('codOferta')

        new_contract = ContractVanzareCumparare(
            vandutDeRadacini=vandutDeRadacini,
            vanzatorPersoanaJuridica=vanzatorPersoanaJuridica,
            cumparatorPersoanaJuridica=cumparatorPersoanaJuridica,
            codAutoturism=codAutoturism,
            codResoinsabilIntocmire=codResoinsabilIntocmire,
            valoareaContractului=valoareaContractului,
            codOferta=codOferta,
            codInternVanzatorPersoanaFizica=codInternVanzatorPersoanaFizica,
            codInternVanzatorPersoanaJuridica=codInternVanzatorPersoanaJuridica,
            codInternCumparatorPersoanaFizica=codInternCumparatorPersoanaFizica,
            codInternCumparatorPersoanaJuridica=codInternCumparatorPersoanaJuridica
        )
        db.session.add(new_contract)
        db.session.commit()
        flash('Contractul a fost creat cu succes!', 'success')
        return redirect(url_for('contracte.list_contracte'))

    return render_template('contracte/create_contract.html', autoturisme=Autoturism.query.all(), 
                           clienti_persoane_fizice=ClientPersoanaFizica.query.all(), 
                           clienti_persoane_juridice=ClientPersoanaJuridica.query.all(), 
                           oferte=OfertaVanzare.query.all())
    
@contracts_bp.route('/edit/<int:codInternContract>', methods=['GET', 'POST'])
@login_required
def edit_contract(codInternContract):
    contract = ContractVanzareCumparare.query.get_or_404(codInternContract)
    autoturisme = Autoturism.query.all()
    clienti_persoane_fizice = ClientPersoanaFizica.query.all()
    clienti_persoane_juridice = ClientPersoanaJuridica.query.all()
    oferte = OfertaVanzare.query.all()

    if request.method == 'POST':
        contract.vandutDeRadacini = bool(request.form.get('vandutDeRadacini'))
        contract.vanzatorPersoanaJuridica = bool(request.form.get('vanzatorPersoanaJuridica'))
        contract.cumparatorPersoanaJuridica = bool(request.form.get('cumparatorPersoanaJuridica'))
        contract.codAutoturism = request.form.get('codAutoturism')
        contract.codInternVanzatorPersoanaFizica = request.form.get('codInternVanzatorPersoanaFizica')
        contract.codInternVanzatorPersoanaJuridica = request.form.get('codInternVanzatorPersoanaJuridica')
        contract.codInternCumparatorPersoanaFizica = request.form.get('codInternCumparatorPersoanaFizica')
        contract.codInternCumparatorPersoanaJuridica = request.form.get('codInternCumparatorPersoanaJuridica')
        contract.valoareaContractului = request.form.get('valoareaContractului')
        contract.codOferta = request.form.get('codOferta')

        db.session.commit()
        flash('Contract updated successfully!', 'success')
        return redirect(url_for('contracte.list_contracts'))

    return render_template('contracte/edit_contract.html', contract=contract, autoturisme=autoturisme, clienti_persoane_fizice=clienti_persoane_fizice, clienti_persoane_juridice=clienti_persoane_juridice, oferte=oferte)

@contracts_bp.route('/delete/<int:codInternContract>', methods=['POST'])
@login_required
def delete_contract(codInternContract):
    contract = ContractVanzareCumparare.query.get_or_404(codInternContract)
    db.session.delete(contract)
    db.session.commit()
    flash('Contract deleted successfully!', 'success')
    return redirect(url_for('contracte.list_contracte'))

@contracts_bp.route('/generate_contract/<int:codInternContract>', methods=['GET'])
@login_required
def generate_contract(codInternContract):
    contract = ContractVanzareCumparare.query.get_or_404(codInternContract)
    rendered_html = render_template(
        'contracte/contract.html',
        contract=contract,
        logo_url=url_for('static', filename='images/logo.jpg', _external=True) ,
        valInNumere=num2words(contract.valoareaContractului, lang='ro')
        )

    directory = 'C:\\Contracte'
    if not os.path.exists(directory):
        os.makedirs(directory)

    pdf_file = pdfkit.from_string(rendered_html, False)

    pdf_path = os.path.join(directory, f'contract_{contract.codInternContract}.pdf')
    with open(pdf_path, 'wb') as f:
        f.write(pdf_file)

    return send_file(pdf_path, as_attachment=True)