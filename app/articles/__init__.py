from flask import Blueprint

bp = Blueprint('articles', __name__)

from . import models, forms, routes
