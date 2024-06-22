from flask import Blueprint

teste_bp = Blueprint('teste', __name__)

from . import routes
