from flask import Blueprint

autoturism_bp = Blueprint('autoturism', __name__, template_folder='templates/autoturism')

from blueprints.autoturism import routes
