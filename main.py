from flask import Flask, redirect, url_for, render_template, request
from flask_login import LoginManager, login_required
from db import db
from routes import user_bp

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

@app.route("/")
def homePage():
    user = Utilizator(
        email="mihai.madalin@gmail.com",
        parola="Parola_01",
        rol=1,
        nume="Neculai",
        prenume="Mihaita-Madalin",
        serieActIdentitate="BR",
        numarActIdentate="123445",
        reseteazaParola=True
    )
    db.session.add(user)
    db.session.commit()
    return render_template("/pages/index.html")

@app.route("/users")
@login_required
def list_users():
    page = request.args.get('page', 1, type=int)
    users = Utilizator.query.paginate(page=page, per_page=10)
    return render_template("/pages/users.html", users=users)

@login_manager.user_loader
def load_user(user_id):
    return Utilizator.query.get(int(user_id))

if __name__ == "__main__":
    app.run(debug=True)


