from flask import Blueprint

contracts_bp = Blueprint('contracte', __name__)

from . import routes
