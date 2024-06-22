from flask import Blueprint

categorieteste_bp = Blueprint('categorie_teste', __name__)

from . import routes
