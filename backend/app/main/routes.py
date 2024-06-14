from random import randint
from flask import request, jsonify, make_response
from . import bp
from .document_manager import DocumentManager

#from app.tf_idf import find_best_results

dm = DocumentManager()


#qf = find_best_results.queryFinder()


@bp.route('/search', methods=['GET'])
def search():
    if request.method == 'GET':
        query = request.args.get('q')
        print(query, flush=True)

        # Milestone 1
        resp = dm.get_random_documents(amount=3)

        # Milestone 2
        # resp = qf.query_vector_finder(query, 3)

        return jsonify(resp)


@bp.route('/document/', methods=['GET'])
def get_document():
    if request.method == 'GET':
        document_id = request.args.get('id')
        doc = dm.get_document_by_id(document_id)
        print('Get Document id=', document_id)
        if not doc:
            return make_response(jsonify({'error': 'Document not found'}), 404)
        return jsonify(doc)


@bp.route('/word_embeddings/', methods=['POST'])
def get_word_embeddings():
    if request.method == 'POST':
        paragraph = request.json['paragraph']

        word_embeddings = []
        for word in paragraph.split(' '):
            word_embeddings.append(
                {'word': word, 'embedding': create_word_embedding(word)}
            )
        return jsonify({'result': word_embeddings})


def create_word_embedding(word):
    return randint(0, 100), randint(0, 100), randint(0, 100)
