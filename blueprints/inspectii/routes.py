from flask import render_template, request, redirect, url_for, flash, session

from models.total_teste import TotalTeste
from . import inspectii_bp
from db import db
from models.inspectii import Inspectie
from models.programari import Programare
from models.autoturism import Autoturism
from models.inspectiiteste import InspectieTest
from models.teste import Test
from models.categorieteste import CategorieTeste
from flask_login import login_required, current_user
from weasyprint import HTML

@inspectii_bp.route('/', methods=['GET'])
@login_required
def list_inspectii():
    inspectii = Inspectie.query.all()
    return render_template('inspectii/list_inspectii.html', inspectii=inspectii)

@inspectii_bp.route('/create_phase1/<int:codProgramre>', methods=['GET', 'POST'])
@login_required
def create_inspectie_phase1(codProgramre):
    # TODO - DE ADAUGAT INAPOI CAND SUSTIN (VERIFICA DACA ROL == 2 => Inspector Tehnic)
    # if current_user.rol != 2:
    #     flash('Nu aveți permisiunea de a crea o inspecție.', 'danger')
    #     return redirect(url_for('inspectii.list_inspectii'))
    programare = Programare.query.get_or_404(codProgramre)
    if(programare == None):
        flash('Nu putem crea o inspecite, progrmare invalida.', 'danger')
        return redirect(url_for('inspectii.list_inspectii'))
    if(programare.statusProgramre > 2):
        # TODO De redirectionat catre inspecite (VIEW) daca e realizata sau catre lista programari daca e respinsa
        flash('Nu putem crea o inspecite, progrmare invalida.', 'danger')
        return redirect(url_for('inspectii.list_inspectii'))
    autoturismProgrmare = Autoturism.query.get_or_404(programare.codAutoturism)
    if(autoturismProgrmare == None):
        flash('Nu putem crea o inspecite, progrmare invalida -> Autotursim Inexistent.', 'danger')
        return redirect(url_for('inspectii.list_inspectii'))
    
    
    if request.method == 'POST':
        numar_inmatriculare = request.form.get('NumarInmatriculare')
        data_inspectiei = request.form.get('DataInspectiei')
        valoare_odometru = request.form.get('ValoareOdometru')
        cod_responsabil_intocmire = current_user.codUtilizator

        session['inspectie_data'] = {
            'codProgramre': codProgramre,
            'NumarInmatriculare': numar_inmatriculare,
            'DataInspectiei': data_inspectiei,
            'ValoareOdometru': valoare_odometru,
            'codResponsabilIntocmire': cod_responsabil_intocmire
        }
        autoturismProgrmare.numarInmatriculare = numar_inmatriculare
        autoturismProgrmare.valoareOdometru = valoare_odometru
        
        db.session.commit()

        return redirect(url_for('inspectii.create_inspectie_phase2'))

    return render_template('inspectii/create_inspectie_phase1.html', autoturism = autoturismProgrmare)


@inspectii_bp.route('/inspectii/create_phase2', methods=['GET', 'POST'])
@login_required
def create_inspectie_phase2():

    inspectie_data = session.get('inspectie_data')
    if not inspectie_data:
        flash('Informațiile inspecției nu au fost completate corect.', 'danger')
        return redirect(url_for('inspectii.create_inspectie_phase1'))

    categorii_teste = CategorieTeste.query.all()

    if request.method == 'POST':
        selected_categorii = request.form.getlist('categorii')
        session['selected_categorii'] = selected_categorii
        return redirect(url_for('inspectii.create_inspectie_phase3'))

    return render_template('inspectii/create_inspectie_phase2.html', categorii_teste=categorii_teste)

@inspectii_bp.route('/inspectii/create_phase3', methods=['GET', 'POST'])
@login_required
def create_inspectie_phase3():
    if current_user.rol != 3:
        flash('Nu aveți permisiunea de a crea o inspecție.', 'danger')
        return redirect(url_for('inspectii.list_inspectii'))

    inspectie_data = session.get('inspectie_data')
    selected_categorii = session.get('selected_categorii')
    if not inspectie_data or not selected_categorii:
        flash('Informațiile inspecției nu au fost completate corect.', 'danger')
        return redirect(url_for('inspectii.create_inspectie_phase1'))

    if request.method == 'POST':
        new_inspectie = Inspectie(**inspectie_data)
        db.session.add(new_inspectie)
        db.session.commit()

        for test_id in session['selected_teste']:
            rezultat_test = request.form.get(f'rezultat_{test_id}')
            detalii_test = request.form.get(f'detalii_{test_id}', '')
            new_inspectie_test = InspectieTest(codInspectie=new_inspectie.codInspectie, codTest=test_id, rezultatTest=rezultat_test, DetaliiTest=detalii_test)
            db.session.add(new_inspectie_test)

        db.session.commit()
        flash('Inspecție creată cu succes!', 'success')
        
        # Generate the PDF report
        return redirect(url_for('inspectii.generate_report', inspectie_id=new_inspectie.codInspectie))

    teste_details = db.session.query(Test).join(TotalTeste).filter(TotalTeste.codCategorieTest.in_(selected_categorii)).all()
    session['selected_teste'] = [test.codTest for test in teste_details]
    return render_template('inspectii/create_inspectie_phase3.html', teste_details=teste_details)

@inspectii_bp.route('/<int:codInspectie>/edit', methods=['GET', 'POST'])
@login_required
def edit_inspectie(codInspectie):
    inspectie = Inspectie.query.get_or_404(codInspectie)
    if request.method == 'POST':
        inspectie.NumarInmatriculare = request.form.get('NumarInmatriculare')
        inspectie.DataInspectiei = request.form.get('DataInspectiei')
        inspectie.ValoareOdometru = request.form.get('ValoareOdometru')
        db.session.commit()
        flash('Inspecție actualizată cu succes!', 'success')
        return redirect(url_for('inspectii.list_inspectii'))

    return render_template('inspectii/edit_inspectie.html', inspectie=inspectie)

@inspectii_bp.route('/<int:codInspectie>/delete', methods=['POST'])
@login_required
def delete_inspectie(codInspectie):
    if current_user.rol != 3:
        flash('Nu aveți permisiunea de a șterge o inspecție.', 'danger')
        return redirect(url_for('inspectii.list_inspectii'))

    inspectie = Inspectie.query.get_or_404(codInspectie)
    db.session.delete(inspectie)
    db.session.commit()
    flash('Inspecție ștearsă cu succes!', 'success')
    return redirect(url_for('inspectii.list_inspectii'))



@inspectii_bp.route('/generate_report/<int:inspectie_id>', methods=['GET'])
@login_required
def generate_report(inspectie_id):
    inspectie = Inspectie.query.get_or_404(inspectie_id)
    inspectie_tests = InspectieTest.query.filter_by(codInspectie=inspectie_id).all()

    # Prepare data for the template
    inspection_data = inspectie.serialize
    tests = [test.serialize for test in inspectie_tests]

    # Render the template to HTML
    rendered_html = render_template('inspectii/raport.html', inspection_data=inspection_data, tests=tests, logo_url=url_for('static', filename='images/logo.png'))

    # Convert HTML to PDF
    pdf_file = HTML(string=rendered_html).write_pdf()

    # Save the PDF file
    pdf_path = f'/C:/report_{inspectie_id}.pdf'
    with open(pdf_path, 'wb') as f:
        f.write(pdf_file)

    # Serve the PDF to the user
    return send_file(pdf_path, as_attachment=True)
