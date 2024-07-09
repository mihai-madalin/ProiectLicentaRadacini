from flask import Blueprint

facturi_bp = Blueprint('factura_bp', __name__)

from . import routes