from flask import Blueprint

dotari_bp = Blueprint('dotari', __name__, template_folder='templates/dotari')

from blueprints.dotari import routes