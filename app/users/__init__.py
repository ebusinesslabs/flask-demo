from flask import Blueprint, g

bp = Blueprint('users', __name__)

from . import routes, forms