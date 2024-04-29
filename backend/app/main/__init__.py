from flask import Blueprint

bp = Blueprint('main', __name__) 

from . import routes
from . import generate_random_results
