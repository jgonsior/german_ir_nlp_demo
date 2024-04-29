from flask import request
from . import bp
from .generate_random_results import Randomizer


randomizer = Randomizer()

@bp.route('/search', methods=['GET'])
def search():
    if request.method == 'GET':
        query = request.args.get('q')
        print(query, flush=True)

        return randomizer.get_result()
