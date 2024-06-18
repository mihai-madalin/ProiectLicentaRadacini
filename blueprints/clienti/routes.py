from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from db import db
from models.client_persoana_fizica import ClientPersoanaFizica
from models.client_persoana_juridica import ClientPersoanaJuridica
from blueprints.clienti import clienti_bp

@clienti_bp.route("/create_client_persoana_fizica", methods=["GET", "POST"])
@login_required
def create_client_fizica():
    if request.method == "POST":
        data = request.form
        new_client = ClientPersoanaFizica(
            nume=data["nume"],
            prenume=data["prenume"],
            telefon=data["telefon"],
            CNP=data.get("CNP"),
            judet=data.get("judet"),
            oras=data.get("oras"),
            strada=data.get("strada"),
            numar=data.get("numar"),
            bloc=data.get("bloc"),
            scara=data.get("scara"),
            etaj=data.get("etaj"),
            appartament=data.get("appartament")
        )
        db.session.add(new_client)
        db.session.commit()
        flash("Client created successfully.", "success")
        return redirect(url_for("clienti.list_clienti_combined"))
    return render_template("clienti/create_client_persoana_fizica.html")

@clienti_bp.route("/create_client_persoana_juridica", methods=["GET", "POST"])
@login_required
def create_client_juridica():
    if request.method == "POST":
        data = request.form
        new_client = ClientPersoanaJuridica(
            Nume=data["Nume"],
            NumarRegistrulComertului=data.get("NumarRegistrulComertului"),
            CUI=data["CUI"],
            SucursalaBancii=data["SucursalaBancii"],
            IBAN=data["IBAN"],
            Tara=data["Tara"],
            Judet=data.get("Judet"),
            Oras=data["Oras"],
            Strada=data["Strada"],
            Numar=data["Numar"],
            Scara=data.get("Scara"),
            Bloc=data.get("Bloc"),
            Etaj=data.get("Etaj"),
            Apartament=data.get("Apartament"),
            numeReprezentant=data["numeReprezentant"],
            prenumeReprezentant=data["prenumeReprezentant"],
            telefonReprezentant=data["telefonReprezentant"],
            CNPReprezentant=data["CNPReprezentant"],
            judetReprezentant=data.get("judetReprezentant"),
            orasReprezentant=data.get("orasReprezentant"),
            stradaReprezentant=data.get("stradaReprezentant"),
            numarReprezentant=data.get("numarReprezentant"),
            blocReprezentant=data.get("blocReprezentant"),
            scaraReprezentant=data.get("scaraReprezentant"),
            etajReprezentant=data.get("etajReprezentant"),
            appartamentReprezentant=data.get("appartamentReprezentant")
        )
        db.session.add(new_client)
        db.session.commit()
        flash("Client created successfully.", "success")
        return redirect(url_for("clienti.list_clienti_combined"))
    return render_template("clienti/create_client_persoana_juridica.html")

# List ClientPersoanaFizica
@clienti_bp.route("/list_fizici", methods=["GET"])
@login_required
def list_clienti_fizici():
    clienti_fizici = ClientPersoanaFizica.query.all()
    return render_template("clienti/list_clienti_persoana_fizica.html", clienti_fizici=clienti_fizici)

# List ClientPersoanaJuridica
@clienti_bp.route("/list_juridici", methods=["GET"])
@login_required
def list_clienti_juridici():
    clienti_juridici = ClientPersoanaJuridica.query.all()
    return render_template("clienti/list_clienti_persoana_juridica.html", clienti_juridici=clienti_juridici)

# List Combined Clients
@clienti_bp.route("/list_clienti_combined", methods=["GET"])
@login_required
def list_clienti_combined():
    clienti_fizici = ClientPersoanaFizica.query.all()
    clienti_juridici = ClientPersoanaJuridica.query.all()
    combined_clients = [
        {'type': 'fizica', 'name': f"{client.prenume} {client.nume}", 'id': client.codClientPF}
        for client in clienti_fizici
    ] + [
        {'type': 'juridica', 'name': client.Nume, 'id': client.codClientPJ}
        for client in clienti_juridici
    ]
    return render_template("clienti/list_clienti_combined.html", combined_clients=combined_clients)

@clienti_bp.route("/view_persoana_fizica/<int:client_id>", methods=["GET"])
@login_required
def view_client_fizica(client_id):
    client = ClientPersoanaFizica.query.get_or_404(client_id)
    return render_template("clienti/view_client_persoana_fizica.html", client=client)

@clienti_bp.route("/view_persoana_juridica/<int:client_id>", methods=["GET"])
@login_required
def view_client_juridica(client_id):
    client = ClientPersoanaJuridica.query.get_or_404(client_id)
    return render_template("clienti/view_client_persoana_juridica.html", client=client)

@clienti_bp.route("/edit_fizica/<int:client_id>", methods=["GET", "POST"])
@login_required
def edit_client_fizica(client_id):
    client = ClientPersoanaFizica.query.get_or_404(client_id)
    if request.method == "POST":
        data = request.form
        client.nume = data["nume"]
        client.prenume = data["prenume"]
        client.telefon = data["telefon"]
        client.CNP = data.get("CNP")
        client.judet = data.get("judet")
        client.oras = data.get("oras")
        client.strada = data.get("strada")
        client.numar = data.get("numar")
        client.bloc = data.get("bloc")
        client.scara = data.get("scara")
        client.etaj = data.get("etaj")
        client.appartament = data.get("appartament")
        db.session.commit()
        flash("Client updated successfully.", "success")
        return redirect(url_for("clienti.view_client_fizica", client_id=client.codClientPF))
    return render_template("clienti/edit_client_persoana_fizica.html", client=client)

@clienti_bp.route("/edit_juridica/<int:client_id>", methods=["GET", "POST"])
@login_required
def edit_client_juridica(client_id):
    client = ClientPersoanaJuridica.query.get_or_404(client_id)
    if request.method == "POST":
        data = request.form
        client.Nume = data["Nume"]
        client.NumarRegistrulComertului = data.get("NumarRegistrulComertului")
        client.CUI = data["CUI"]
        client.SucursalaBancii = data["SucursalaBancii"]
        client.IBAN = data["IBAN"]
        client.Tara = data["Tara"]
        client.Judet = data.get("Judet")
        client.Oras = data["Oras"]
        client.Strada = data["Strada"]
        client.Numar = data["Numar"]
        client.Scara = data.get("Scara")
        client.Bloc = data.get("Bloc")
        client.Etaj = data.get("Etaj")
        client.Apartament = data.get("Apartament")
        client.numeReprezentant = data["numeReprezentant"]
        client.prenumeReprezentant = data["prenumeReprezentant"]
        client.telefonReprezentant = data["telefonReprezentant"]
        client.CNPReprezentant = data["CNPReprezentant"]
        client.judetReprezentant = data.get("judetReprezentant")
        client.orasReprezentant = data.get("orasReprezentant")
        client.stradaReprezentant = data.get("stradaReprezentant")
        client.numarReprezentant = data.get("numarReprezentant")
        client.blocReprezentant = data.get("blocReprezentant")
        client.scaraReprezentant = data.get("scaraReprezentant")
        client.etajReprezentant = data.get("etajReprezentant")
        client.appartamentReprezentant = data.get("appartamentReprezentant")
        db.session.commit()
        flash("Client updated successfully.", "success")
        return redirect(url_for("clienti.view_client_juridica", client_id=client.codClientPJ))
    return render_template("clienti/edit_client_persoana_juridica.html", client=client)


@clienti_bp.route("/delete_client_fizica/<int:client_id>", methods=["POST"])
@login_required
def delete_client_fizica(client_id):
    client = ClientPersoanaFizica.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    flash("Clientul persoană fizică a fost șters cu succes", "success")
    return redirect(url_for('clienti.list_clienti_fizici'))

@clienti_bp.route("/delete_client_juridica/<int:client_id>", methods=["POST"])
@login_required
def delete_client_juridica(client_id):
    client = ClientPersoanaJuridica.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    flash("Clientul persoană juridică a fost șters cu succes", "success")
    return redirect(url_for('clienti.list_clienti_juridici'))