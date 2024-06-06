from flask import Blueprint

bp = Blueprint('tf_idf', __name__)

from . import find_best_results
