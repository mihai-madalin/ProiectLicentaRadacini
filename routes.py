# app/blueprints/user/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models.utilizatori import Utilizator
from db import db

user_bp = Blueprint('user', __name__, template_folder='templates/user')

@user_bp.route("/register", methods=["GET", "POST"])
def register():
    print(generate_password_hash("Parola_01"))
    if request.method == "POST":
        email = request.form["email"]
        parola = generate_password_hash(request.form["parola"])
        rol = request.form["rol"]
        nume = request.form["nume"]
        prenume = request.form["prenume"]
        serieActIdentitate = request.form["serieActIdentitate"]
        numarActIdentate = request.form["numarActIdentate"]
        reseteazaParola = request.form.get("reseteazaParola") == "on"
        
        user = Utilizator(
            email=email,
            parola=parola,
            rol=int(rol),
            nume=nume,
            prenume=prenume,
            serieActIdentitate=serieActIdentitate,
            numarActIdentate=numarActIdentate,
            reseteazaParola=reseteazaParola
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user.list_users"))
    return render_template("register.html")

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        parola = request.form["parola"]
        user = Utilizator.query.filter_by(email=email).first()
        if user and check_password_hash(user.parola, parola):
            login_user(user)
            return redirect(url_for("user.list_users"))
        else:
            flash("Login failed. Check your email and password.")
    return render_template("login.html")

@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("user.login"))

@user_bp.route("/users")
@login_required
def list_users():
    if current_user.rol != 3:
        flash("You do not have permission to view this page.")
        return redirect(url_for("user.login"))
    page = request.args.get('page', 1, type=int)
    users = Utilizator.query.paginate(page=page, per_page=10)
    return render_template("users.html", users=users)
