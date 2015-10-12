from flask import Blueprint

api_common = Blueprint('api_common', __name__)

from . import common
