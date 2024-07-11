from flask import render_template, request, redirect, url_for, flash
from . import programari_bp
from db import db
from models.programari import Programare
from models.inspectii import Inspectie
from models.autoturism import Autoturism
from models.client_persoana_fizica import ClientPersoanaFizica
from models.client_persoana_juridica import ClientPersoanaJuridica
from models.utilizatori import Utilizator
from flask_login import current_user, login_required

@programari_bp.route('/', methods=['GET'])
@login_required
def list_programari():
    if current_user.rol == 4:
        programari = Programare.query.all()
    else:
        programari = Programare.query.filter_by(codResponsabilIntocmire=current_user.codUtilizator).all()
    
    for programare in programari:
        programare.autoturism = Autoturism.query.get(programare.codAutoturism)
        if programare.codClientPersoanaFizica:
            programare.client = ClientPersoanaFizica.query.get(programare.codClientPersoanaFizica)
        else:
            programare.client = ClientPersoanaJuridica.query.get(programare.codClientPersoanaJuridica)
        programare.responsabil = Utilizator.query.get(programare.codResponsabilIntocmire)
    
    contor = 0

    NUMAR_TOTAL_KM = 0
    # Pentru a afisa valorile dintr-un obiect 


    # Am 10 masini cu cate un anumit numar x de KM
    # colectia este masini

    # Variabila in care stochez numarul total de km este NR_TOTAL_KM

    # for masina in masini:
    #     NUMAR_TOTAL_KM = NUMAR_TOTAL_KM + masina.valoareOdometru


    for iterator in programari:
        contor = contor +1
    
    numarpgvizionare = contor
    return render_template('programari/list_programari.html', programari=programari, numarpgvizionare=numarpgvizionare)

@programari_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_programare():
    autoturisme = Autoturism.query.filter(Autoturism.status < 4).all()
    clienti_persoane_fizice = ClientPersoanaFizica.query.all()
    clienti_persoane_juridice = ClientPersoanaJuridica.query.all()

    if request.method == 'POST':
        tipProgramare = request.form.get('tipProgramare')
        dataProgramare = request.form.get('dataProgramare')
        codAutoturism = request.form.get('codAutoturism')
        statusProgramre = request.form.get('statusProgramre')
        clientType = request.form.get('clientType')
        codClientPF = request.form.get('codClientPF')
        codClientPJ = request.form.get('codClientPJ')
        codResponsabilIntocmire = current_user.codUtilizator

        if clientType == 'pf':
            codClientPersoanaFizica = codClientPF
            codClientPersoanaJuridica = None
        else:
            codClientPersoanaFizica = None
            codClientPersoanaJuridica = codClientPJ

        new_programare = Programare(
            tipProgramre=tipProgramare,
            dataProgramare=dataProgramare,
            codAutoturism=codAutoturism,
            statusProgramre=statusProgramre,
            codClientPersoanaFizica=codClientPersoanaFizica,
            codClientPersoanaJuridica=codClientPersoanaJuridica,
            codResponsabilIntocmire=codResponsabilIntocmire
        )
        db.session.add(new_programare)
        db.session.commit()
        flash('Programare created successfully!', 'success')
        return redirect(url_for('programari.list_programari'))
    
    return render_template('programari/create_programare.html', autoturisme=autoturisme, clienti_persoane_fizice=clienti_persoane_fizice, clienti_persoane_juridice=clienti_persoane_juridice)

@programari_bp.route('/edit/<int:programare_id>', methods=['GET', 'POST'])
@login_required
def edit_programare(programare_id):
    programare = Programare.query.get_or_404(programare_id)
    autoturisme = Autoturism.query.filter(Autoturism.status < 4).all()
    
    if programare.codClientPersoanaFizica:
        programare.client = ClientPersoanaFizica.query.get(programare.codClientPersoanaFizica)
    else:
        programare.client = ClientPersoanaJuridica.query.get(programare.codClientPersoanaJuridica)
    
    programare.responsabil = Utilizator.query.get(programare.codResponsabilIntocmire)
    
    if (programare.tipProgramre == 1):
        # Fetch  Vizionare
        codOperatiune = None
        print()
    elif (programare.tipProgramre == 2 and programare.statusProgramre in [1,2,3]):
        # Fetch Inspectie
        codProgramare = db.session.query(Inspectie.codInspectie).filter_by(codProgramre=programare_id).first()        
        codOperatiune = codProgramare[0] if codProgramare != None else -1
    else:
        codOperatiune = None

    if request.method == 'POST':
        if programare.statusProgramre not in [3, 4]:
            programare.tipProgramre = request.form.get('tipProgramare')
            programare.dataProgramare = request.form.get('dataProgramare')
            programare.codAutoturism = request.form.get('codAutoturism')
            programare.statusProgramre = request.form.get('statusProgramre')

            codClient = request.form.get('codClient')
            if programare.codClientPersoanaFizica:
                programare.codClientPersoanaFizica = codClient
            else:
                programare.codClientPersoanaJuridica = codClient

            db.session.commit()
            flash('Programare actualizată cu succes!', 'success')
            return redirect(url_for('programari.list_programari'))
    
    return render_template(
        'programari/edit_programare.html',
        programare=programare,
        autoturisme=autoturisme,
        codOperatiune = codOperatiune,
        userRole = current_user.rol
    )