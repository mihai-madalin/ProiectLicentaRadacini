from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from db import db
from models.dotari import Dotare
from flask_login import login_required
from blueprints.dotari import dotari_bp


@dotari_bp.route("/list", methods=["GET"])
@login_required
def list_dotari():
    dotari = Dotare.query.all()
    return render_template("dotari/list_dotari.html", dotari=dotari)

@dotari_bp.route("/create", methods=["POST"])
@login_required
def create_dotare():
    denumireDotare = request.form.get('denumireDotare')
    if denumireDotare:
        new_dotare = Dotare(denumireDotare=denumireDotare)
        db.session.add(new_dotare)
        db.session.commit()
        flash("Dotare created successfully", "success")
    else:
        flash("Denumire Dotare is required", "danger")
    return redirect(url_for("dotari.list_dotari"))

@dotari_bp.route("/edit/<int:codDotare>", methods=["POST"])
@login_required
def edit_dotare(codDotare):
    dotare = Dotare.query.get_or_404(codDotare)
    dotare.denumireDotare = request.form.get('denumireDotare')
    db.session.commit()
    flash("Dotare updated successfully", "success")
    return redirect(url_for("dotari.list_dotari"))

@dotari_bp.route("/delete/<int:codDotare>", methods=["POST"])
@login_required
def delete_dotare(codDotare):
    dotare = Dotare.query.get_or_404(codDotare)
    db.session.delete(dotare)
    db.session.commit()
    flash("Dotare deleted successfully", "success")
    return redirect(url_for("dotari.list_dotari"))
