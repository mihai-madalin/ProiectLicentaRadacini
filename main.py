from flask import Flask, redirect, url_for, render_template, request
from flask_login import LoginManager, login_required, current_user
from db import db
from blueprints.user import user_bp
from blueprints.autoturism import autoturism_bp
from blueprints.clienti import clienti_bp
from blueprints.dotari import dotari_bp
from blueprints.programari import programari_bp
from blueprints.teste import teste_bp
from blueprints.categorie_teste import categorieteste_bp

from models.utilizatori import Utilizator

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ThisIsThePassword_01@localhost/radacini_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Licenta'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login' 

app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(autoturism_bp, url_prefix='/autoturism')
app.register_blueprint(clienti_bp, url_prefix='/clienti')
app.register_blueprint(dotari_bp, url_prefix='/dotari')
app.register_blueprint(programari_bp, url_prefix='/programari')
app.register_blueprint(teste_bp, url_prefix='/teste')
app.register_blueprint(categorieteste_bp, url_prefix='/categorie-teste')

@app.route("/")
def homePage():
    return render_template("/pages/index.html")

@login_manager.user_loader
def load_user(user_id):
    return Utilizator.query.get(int(user_id))

if __name__ == "__main__":
    app.run(debug=True)


