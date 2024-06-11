from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models.utilizatori import Utilizator
from db import db
from blueprints.user import user_bp

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
    return render_template("user/register.html")

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        parola = request.form["parola"]
        user = Utilizator.query.filter_by(email=email).first()
        if user and check_password_hash(user.parola, parola):
            login_user(user)
            flash("Login successful", "success")
            if user.reseteazaParola == True:
                return return_reset_page(user.codUtilizator)
            else:
                return redirect(url_for("user.list_users"))
        else:
            flash("Login failed. Check your email and password.", 'danger')
    return render_template("user/login.html")

@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("user.login"))

@user_bp.route("/list")
@login_required
def list_users():
    if current_user.rol != 4:
        flash(f"You do not have permission to view this page. Ai drepturi de: {current_user.rol}", "warning")
        return redirect(url_for("user.login"))
    page = request.args.get('page', 1, type=int)
    users = Utilizator.query.paginate(page=page, per_page=10)
    return render_template("user/users.html", users=users)


@user_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    print(current_user.codUtilizator == user_id)
    if (current_user.rol != 4 and current_user.codUtilizator != user_id):
        flash(f"Nu ai acces la aceasta pagina. Ai drepturi de: {current_user.rol}", "warning")
        return redirect(url_for("user.login"))
    user = Utilizator.query.get_or_404(user_id)
    if request.method == "POST":
        user.email = request.form["email"]
        if "parola" in request.form and request.form["parola"]:
            user.parola = generate_password_hash(request.form["parola"])
        if current_user.rol == 4:
            user.rol = request.form["rol"]
        user.nume = request.form["nume"]
        user.prenume = request.form["prenume"]
        user.serieActIdentitate = request.form["serieActIdentitate"]
        user.numarActIdentate = request.form["numarActIdentate"]
        
        db.session.commit()
        flash("User updated successfully", "success")
        return redirect(url_for("user.list_users"))
    return render_template("user/edit_user.html", user=user)


@user_bp.route("/delete/<int:user_id>", methods=["GET", "POST"])
@login_required
def remove_user(user_id):
    if current_user.rol !=3:
        flash(f"You do not have permission to view this page. Ai drepturi de: {current_user.rol}", "warning")
        return redirect(url_for("user.login"))
    
    user = db.session.query(Utilizator).get(user_id)
    if user != None:
        db.session.delete(user)
        db.session.commit()
    else:
        flash(f"Current user is unavailable", "warning")
        
    return list_users()

@user_bp.route("/reset_password/<int:user_id>", methods=["GET", "POST"])
def reset_password(user_id):
    user = Utilizator.query.get_or_404(user_id)
    if request.method == "POST":
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]
        
        if new_password != confirm_password:
            flash("Passwords do not match. Please try again.", "danger")
        else:
            user.parola = generate_password_hash(new_password)
            user.reseteazaParola = False
            db.session.commit()
            flash("Password updated successfully", "success")
            return redirect(url_for("homePage"))


def return_reset_page(user_id):
    user = Utilizator.query.get_or_404(user_id)
    return render_template("user/reset_password.html", user=user)



@user_bp.route('/profile')
@login_required
def profile():
    role_names = {
        1: "Agent Vanzari",
        2: "Inspector Tehnic",
        3: "Departament Financiar",
        4: "Administrator"
    }
    user = current_user
    user.rol_name = role_names.get(user.rol, "Rol neidentificat")
    
    return render_template('user/profile.html', user=user)