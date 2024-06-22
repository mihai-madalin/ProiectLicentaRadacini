from flask import render_template, request, redirect, url_for, flash, session

from models.total_teste import TotalTeste
from . import inspectii_bp
from db import db
from models.inspectii import Inspectie
from models.inspectiiteste import InspectieTest
from models.teste import Test
from models.categorieteste import CategorieTeste
from flask_login import login_required, current_user

@inspectii_bp.route('/', methods=['GET'])
@login_required
def list_inspectii():
    inspectii = Inspectie.query.all()
    return render_template('inspectii/list_inspectii.html', inspectii=inspectii)

@inspectii_bp.route('/create_phase1/<int:codProgramre>', methods=['GET', 'POST'])
@login_required
def create_inspectie_phase1(codProgramre):
    if current_user.rol < 3:
        flash('Nu aveți permisiunea de a crea o inspecție.', 'danger')
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

        return redirect(url_for('inspectii.create_inspectie_phase2'))

    return render_template('inspectii/create_inspectie_phase1.html')

@inspectii_bp.route('/create_phase2', methods=['GET', 'POST'])
@login_required
def create_inspectie_phase2():
    if current_user.rol < 3:
        flash('Nu aveți permisiunea de a crea o inspecție.', 'danger')
        return redirect(url_for('inspectii.list_inspectii'))

    inspectie_data = session.get('inspectie_data')
    if not inspectie_data:
        flash('Informațiile inspecției nu au fost completate corect.', 'danger')
        return redirect(url_for('inspectii.list_inspectii'))

    categorii_teste = CategorieTeste.query.all()
    

    if request.method == 'POST':
        new_inspectie = Inspectie(**inspectie_data)
        db.session.add(new_inspectie)
        db.session.commit()

        for categorie in categorii_teste:
            teste_ids = request.form.getlist(f'teste_{categorie.codCategorieTeste}')
            for test_id in teste_ids:
                rezultat_test = request.form.get(f'rezultat_{test_id}')
                detalii_test = request.form.get(f'detalii_{test_id}', '')
                new_inspectie_test = InspectieTest(codInspectie=new_inspectie.codInspectie, codTest=test_id, rezultatTest=rezultat_test, DetaliiTest=detalii_test)
                db.session.add(new_inspectie_test)

        db.session.commit()
        flash('Inspecție creată cu succes!', 'success')
        return redirect(url_for('inspectii.list_inspectii'))

    return render_template('inspectii/create_inspectie_phase2.html', categorii_teste=categorii_teste)

@inspectii_bp.route('/<int:codInspectie>/edit', methods=['GET', 'POST'])
@login_required
def edit_inspectie(codInspectie):
    if current_user.rol != 3:
        flash('Nu aveți permisiunea de a edita o inspecție.', 'danger')
        return redirect(url_for('inspectii.list_inspectii'))

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
