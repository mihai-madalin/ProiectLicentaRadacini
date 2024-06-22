from flask import Blueprint

inspectii_bp = Blueprint('inspectii', __name__)

from . import routes
