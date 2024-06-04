from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from db import db

from models.utilizatori import Utilizator

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ThisIsThePassword_01@localhost/radacini_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

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
def list_users():
    users = Utilizator.query.all()
    return render_template("/pages/users.html", users=users)

if __name__ == "__main__":
    app.run(debug=True)

if( __name__ == "__main__"):
	app.run(debug=True)


