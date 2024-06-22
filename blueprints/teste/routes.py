from flask import render_template, request, redirect, url_for, flash
from . import teste_bp
from db import db
from models.teste import Test
from models.categorieteste import CategorieTeste
from models.total_teste import TotalTeste
from flask_login import login_required

@teste_bp.route('/', methods=['GET'])
@login_required
def list_teste():
    teste = Test.query.all()
    return render_template('/teste/list_teste.html', teste=teste)

@teste_bp.route('/teste/create', methods=['POST'])
@login_required
def create_test():
    if request.method == 'POST':
        denumire_test = request.form.get('denumireTest')
        new_test = Test(DenumireTest=denumire_test)
        db.session.add(new_test)
        db.session.commit()
        flash('Test creat cu succes!', 'success')
        return redirect(url_for('teste.list_teste'))

@teste_bp.route('/<int:codTest>/edit', methods=['POST'])
@login_required
def edit_test(codTest):
    test = Test.query.get_or_404(codTest)
    if request.method == 'POST':
        test.DenumireTest = request.form.get('denumireTest')
        db.session.commit()
        flash('Test actualizat cu succes!', 'success')
        return redirect(url_for('teste.list_teste'))

@teste_bp.route('/<int:codTest>/delete', methods=['POST'])
@login_required
def delete_test(codTest):
    test = Test.query.get_or_404(codTest)
    db.session.delete(test)
    db.session.commit()
    flash('Test șters cu succes!', 'success')
    return redirect(url_for('teste.list_teste'))