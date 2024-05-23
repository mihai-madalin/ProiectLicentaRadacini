from flask import Flask, redirect, url_for, render_template
import mysql.connector

app = Flask(__name__)

@app.route("/")
def homePage():
    con = mysql.connector.connect(host="localhost", user = "root", password="ThisIsThePassword_01", database="radacini_db")
    cursor = con.cursor();
    cursor.execute("SELECT * FROM radacini_db.utilizatori")
    records = cursor.fetchall()
    print(records)
    return render_template("/pages/index.html")




if( __name__ == "__main__"):
	app.run(debug=True)


