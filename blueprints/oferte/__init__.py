from flask import Blueprint

oferte_vanzare_bp = Blueprint('oferte_vanzare', __name__)

from . import routes
