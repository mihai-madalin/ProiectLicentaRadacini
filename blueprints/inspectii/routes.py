import pdfkit
import os
from flask import render_template, request, redirect, send_file, url_for, flash, session
from models.total_teste import TotalTeste
from . import inspectii_bp
from db import db
from models.inspectii import Inspectie
from models.programari import Programare
from models.autoturism import Autoturism
from models.inspectiiteste import InspectieTest
from models.teste import Test
from models.categorieteste import CategorieTeste
from models.utilizatori import Utilizator
from flask_login import login_required, current_user

# Path to wkhtmltopdf executable
path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

@inspectii_bp.route('/', methods=['GET'])
@login_required
def list_inspectii():
    inspectii = Inspectie.query.all()
    for inspectie in inspectii:
        responsabil = Utilizator.query.get(inspectie.codResponsabilIntocmire)
        inspectie.ResponsabilNume = f"{responsabil.nume} {responsabil.prenume}"
    return render_template('inspectii/list_inspectii.html', inspectii=inspectii)

@inspectii_bp.route('/create_phase1/<int:codProgramre>', methods=['GET', 'POST'])
@login_required
def create_inspectie_phase1(codProgramre):
    if current_user.rol != 2:
        flash('Nu aveți permisiunea de a crea o inspecție.', 'danger')
        return redirect(url_for('inspectii.list_inspectii'))

    programare = Programare.query.get_or_404(codProgramre)
    autoturismProgrmare = Autoturism.query.get_or_404(programare.codAutoturism)

    if request.method == 'POST':
        numar_inmatriculare = request.form.get('NumarInmatriculare')
        data_inspectiei = request.form.get('DataInspectiei')
        valoare_odometru = request.form.get('ValoareOdometru')
        
        # Add odometer check
        if int(valoare_odometru) < autoturismProgrmare.valoareOdometru:
            flash('Valoarea odometrului introdusă este mai mică decât valoarea actuală.', 'danger')
            return render_template('inspectii/create_inspectie_phase1.html', autoturism=autoturismProgrmare)
        
        cod_responsabil_intocmire = current_user.codUtilizator

        session['inspectie_data'] = {
            'codProgramre': codProgramre,
            'NumarInmatriculare': numar_inmatriculare,
            'DataInspectiei': data_inspectiei,
            'ValoareOdometru': valoare_odometru,
            'codResponsabilIntocmire': cod_responsabil_intocmire
        }

        # Update the car's registration number and odometer value
        autoturismProgrmare.numarInmatriculare = numar_inmatriculare
        autoturismProgrmare.valoareOdometru = valoare_odometru

        db.session.commit()

        return redirect(url_for('inspectii.create_inspectie_phase2'))

    return render_template('inspectii/create_inspectie_phase1.html', autoturism=autoturismProgrmare)

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
            
        programareDeActualizat = Programare.query.get_or_404(new_inspectie.codProgramre)
        programareDeActualizat.statusProgramre = 3    
        db.session.commit()
        flash('Inspecție creată cu succes!', 'success')
        
        return redirect(url_for('inspectii.list_inspectii'))

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

    # Fetch the responsible person's first and last name
    responsabil = Utilizator.query.get(inspectie.codResponsabilIntocmire)
    responsabil_name = f"{responsabil.nume} {responsabil.prenume}"

    # Prepare data for the template
    inspection_data = inspectie.serialize
    inspection_data['ResponsabilNume'] = responsabil_name

    # Group tests by categories
    tests_by_category = {}
    for test in inspectie_tests:
        test_details = Test.query.get(test.codTest)
        test_category = TotalTeste.query.filter_by(codTest=test.codTest).first().codCategorieTest
        category_name = CategorieTeste.query.get(test_category).DenumireCategorieTeste

        # Replace test result numbers with descriptions
        if test.rezultatTest == 1:
            result_description = 'Trecut'
        elif test.rezultatTest == 2:
            result_description = 'Defectiune Minora'
        elif test.rezultatTest == 3:
            result_description = 'Defectiune Majora'
        else:
            result_description = 'N/A'

        test_data = {
            'DenumireTest': test_details.DenumireTest,
            'RezultatTest': result_description,
            'DetaliiTest': test.DetaliiTest
        }

        if category_name not in tests_by_category:
            tests_by_category[category_name] = []
        if test_data not in tests_by_category[category_name]:
            tests_by_category[category_name].append(test_data)

    # Render the template to HTML
    logo_url = url_for('static', filename='images/logo.jpg', _external=True)
    rendered_html = render_template('inspectii/raport.html', inspection_data=inspection_data, tests_by_category=tests_by_category, logo_url=logo_url)

    # Ensure the directory exists
    reports_dir = 'C:\\Rapoarte'
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)

    # Convert HTML to PDF
    pdf_file = pdfkit.from_string(rendered_html, False, configuration=config)

    # Save the PDF file
    pdf_path = os.path.join(reports_dir, f'report_{inspectie_id}.pdf')
    with open(pdf_path, 'wb') as f:
        f.write(pdf_file)

    # Serve the PDF to the user
    return send_file(pdf_path, as_attachment=True)
