from flask import Blueprint

clienti_bp = Blueprint('clienti', __name__, template_folder='templates/clienti')

from blueprints.clienti import routes
