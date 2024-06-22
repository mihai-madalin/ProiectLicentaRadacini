from flask import render_template, request, redirect, url_for, flash
from . import categorieteste_bp
from db import db
from models.categorieteste import CategorieTeste
from models.total_teste import TotalTeste
from models.teste import Test
from flask_login import login_required

@categorieteste_bp.route('/', methods=['GET'])
@login_required
def list_categorii_teste():
    categorii = CategorieTeste.query.all()
    return render_template('categorie_teste/list_categorii_teste.html', categorii=categorii)

@categorieteste_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_categorie_teste():
    if request.method == 'POST':
        denumire_categorie = request.form.get('denumireCategorieTeste')
        teste_ids = request.form.getlist('teste_ids')

        new_categorie = CategorieTeste(DenumireCategorieTeste=denumire_categorie)
        db.session.add(new_categorie)
        db.session.commit()

        for test_id in teste_ids:
            new_total_test = TotalTeste(codCategorieTest=new_categorie.codCategorieTeste, codTest=test_id)
            db.session.add(new_total_test)

        db.session.commit()
        flash('Categorie Teste creată cu succes!', 'success')
        return redirect(url_for('categorie_teste.list_categorii_teste'))

    teste = Test.query.all()
    return render_template('categorie_teste/edit_categorie_teste.html', teste=teste)

@categorieteste_bp.route('/edit/<int:codCategorieTeste>', methods=['GET', 'POST'])
@login_required
def edit_categorie_teste(codCategorieTeste):
    categorie = CategorieTeste.query.get_or_404(codCategorieTeste)
    if request.method == 'POST':
        categorie.DenumireCategorieTeste = request.form.get('denumireCategorieTeste')
        teste_ids = request.form.getlist('teste_ids')

        TotalTeste.query.filter_by(codCategorieTest=codCategorieTeste).delete()
        for test_id in teste_ids:
            new_total_test = TotalTeste(codCategorieTest=codCategorieTeste, codTest=test_id)
            db.session.add(new_total_test)

        db.session.commit()
        flash('Categorie Teste actualizată cu succes!', 'success')
        return redirect(url_for('categorie_teste.list_categorii_teste'))

    teste = Test.query.all()
    selected_tests = [t.codTest for t in TotalTeste.query.filter_by(codCategorieTest=codCategorieTeste).all()]
    return render_template('categorie_teste/edit_categorie_teste.html', categorie=categorie, teste=teste, selected_tests=selected_tests)

@categorieteste_bp.route('/delete/<int:codCategorieTeste>', methods=['POST'])
@login_required
def delete_categorie_teste(codCategorieTeste):
    categorie = CategorieTeste.query.get_or_404(codCategorieTeste)
    db.session.delete(categorie)
    db.session.commit()
    flash('Categorie Teste ștearsă cu succes!', 'success')
    return redirect(url_for('teste.list_categorii_teste'))
