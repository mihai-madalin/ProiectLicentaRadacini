from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
import os
from db import db
from models.tipautoturisme import TipAutoturism
from models.autoturism import Autoturism
from models.autoturisme_dotari import AutoturismDotari
from models.autoturisme_fotografii import AutoturismFotografii
from blueprints.autoturism import autoturism_bp

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def get_tip_autoturism(codTipAutoturism):
    if codTipAutoturism != None:
        tipAutoturism = db.session.query(TipAutoturism).get(codTipAutoturism)
        return tipAutoturism.denumireTipAutoturisme
    else:
        return "Tip neidentificat" 

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@autoturism_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_autoturism():
    if request.method == "POST":
        data = request.form
        new_autoturism = Autoturism(
            marca=data["marca"],
            model=data["model"],
            valoareOdometru=data["valoareOdometru"],
            tipAutoturism=data["tipAutoturism"],
            AnulFabricatiei=data["AnulFabricatiei"],
            serieCaroserie=data["serieCaroserie"],
            numarInmatriculare=data["numarInmatriculare"],
            culoare=data["culoare"],
            dataPrimeiImatirculari=data["dataPrimeiImatirculari"],
            capacitateCilindrica=data["capacitateCilindrica"],
            combustibil=data["combustibil"],
            numarPropietariAnteriori=data["numarPropietariAnteriori"],
            capacitateRezervorTermic=data.get("capacitateRezervorTermic"),
            capacitateAutonomieBaterie=data.get("capacitateAutonomieBaterie"),
            putereMotor=data["putereMotor"],
            tipTransmisie=data["tipTransmisie"],
            status=data["status"]
        )
        db.session.add(new_autoturism)
        db.session.commit()
        flash("Autoturism created successfully.", "success")
        return redirect(url_for("autoturism.list_autoturism"))
    return render_template("autoturism/create_autoturism.html")

@autoturism_bp.route("/list", methods=["GET"])
@login_required
def list_autoturism():
    autoturisme = Autoturism.query.all()
    return render_template("autoturism/list_autoturism.html", autoturisme=autoturisme)

@autoturism_bp.route("/view/<int:autoturism_id>", methods=["GET"])
@login_required
def view_autoturism(autoturism_id):
    autoturism = Autoturism.query.get_or_404(autoturism_id)
    photos = db.session.query(AutoturismFotografii).where(AutoturismFotografii.codAutoturism == autoturism_id)
    
    return render_template("autoturism/view_autoturism.html", 
                            autoturism=autoturism,
                            fotografii = photos,
                            tipAutoturism = get_tip_autoturism(autoturism.tipAutoturism))

# @autoturism_bp.route("/edit/<int:autoturism_id>", methods=["GET", "POST"])
# @login_required
# def edit_autoturism(autoturism_id):
#     autoturism = Autoturism.query.get_or_404(autoturism_id)
#     if request.method == "POST":
#         data = request.form
#         autoturism.marca = data["marca"]
#         autoturism.model = data["model"]
#         autoturism.valoareOdometru = data["valoareOdometru"]
#         autoturism.tipAutoturism = data["tipAutoturism"]
#         autoturism.AnulFabricatiei = data["AnulFabricatiei"]
#         autoturism.serieCaroserie = data["serieCaroserie"]
#         autoturism.numarInmatriculare = data["numarInmatriculare"]
#         autoturism.culoare = data["culoare"]
#         autoturism.dataPrimeiImatirculari = data["dataPrimeiImatirculari"]
#         autoturism.capacitateCilindrica = data["capacitateCilindrica"]
#         autoturism.combustibil = data["combustibil"]
#         autoturism.numarPropietariAnteriori = data["numarPropietariAnteriori"]
#         autoturism.capacitateRezervorTermic = data.get("capacitateRezervorTermic")
#         autoturism.capacitateAutonomieBaterie = data.get("capacitateAutonomieBaterie")
#         autoturism.putereMotor = data["putereMotor"]
#         autoturism.tipTransmisie = data["tipTransmisie"]
#         autoturism.status = data["status"]
#         db.session.commit()
#         flash("Autoturism updated successfully.", "success")
#         return redirect(url_for("autoturism.list_autoturism"))
#     return render_template("autoturism/edit_autoturism.html", autoturism=autoturism)

@autoturism_bp.route("/delete/<int:autoturism_id>", methods=["POST"])
@login_required
def delete_autoturism(autoturism_id):
    autoturism = Autoturism.query.get_or_404(autoturism_id)
    db.session.delete(autoturism)
    db.session.commit()
    flash("Autoturism deleted successfully.", "success")
    return redirect(url_for("autoturism.list_autoturism"))

@autoturism_bp.route("/upload_photos/<int:autoturism_id>", methods=["GET", "POST"])
@login_required
def upload_photos(autoturism_id):
    autoturism = Autoturism.query.get_or_404(autoturism_id)
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            relative_filepath = 'uploads/autoturisme/' + filename
            absolute_filepath = os.path.join(current_app.root_path, 'static', relative_filepath)
            os.makedirs(os.path.dirname(absolute_filepath), exist_ok=True)
            file.save(absolute_filepath)
            new_photo = AutoturismFotografii(codAutoturism=autoturism_id, caleDiscFotografie=relative_filepath, fotografiePrincipala=False)
            db.session.add(new_photo)
            db.session.commit()
            flash('Photo uploaded successfully', 'success')
            return redirect(url_for('autoturism.view_autoturism', autoturism_id=autoturism_id))
    return render_template("autoturism/upload_photos.html", autoturism=autoturism)

@autoturism_bp.route("/edit/<int:autoturism_id>", methods=["GET", "POST"])
@login_required
def edit_autoturism(autoturism_id):
    autoturism = Autoturism.query.get_or_404(autoturism_id)
    if request.method == "POST":
        data = request.form
        autoturism.marca = data["marca"]
        autoturism.model = data["model"]
        autoturism.valoareOdometru = data["valoareOdometru"]
        # autoturism.tipAutoturism = data["tipAutoturism"]
        autoturism.AnulFabricatiei = data["AnulFabricatiei"]
        autoturism.serieCaroserie = data["serieCaroserie"]
        autoturism.numarInmatriculare = data["numarInmatriculare"]
        autoturism.culoare = data["culoare"]
        autoturism.dataPrimeiImatirculari = data["dataPrimeiImatirculari"]
        autoturism.capacitateCilindrica = data["capacitateCilindrica"]
        autoturism.combustibil = data["combustibil"]
        autoturism.numarPropietariAnteriori = data["numarPropietariAnteriori"]
        autoturism.capacitateRezervorTermic = data.get("capacitateRezervorTermic")
        autoturism.capacitateAutonomieBaterie = data.get("capacitateAutonomieBaterie")
        autoturism.putereMotor = data["putereMotor"]
        # autoturism.tipTransmisie = data["tipTransmisie"]
        autoturism.status = data["status"]
        db.session.commit()
        flash("Autoturism updated successfully.", "success")
        
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                relative_filepath = 'uploads/autoturisme/' + filename
                absolute_filepath = os.path.join(current_app.root_path, 'static', relative_filepath)
                os.makedirs(os.path.dirname(absolute_filepath), exist_ok=True)
                file.save(absolute_filepath)
                new_photo = AutoturismFotografii(codAutoturism=autoturism_id, caleDiscFotografie=relative_filepath, fotografiePrincipala=False)
                db.session.add(new_photo)
                db.session.commit()
                flash('Photo uploaded successfully', 'success')
        return redirect(url_for("autoturism.view_autoturism", autoturism_id=autoturism_id))
    photos = db.session.query(AutoturismFotografii).where(AutoturismFotografii.codAutoturism == autoturism_id)
    return render_template("autoturism/edit_autoturism.html", autoturism=autoturism, fotografii=photos)