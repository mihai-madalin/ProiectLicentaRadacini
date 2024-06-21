from flask import Blueprint

programari_bp = Blueprint('programari', __name__)

from . import routes
