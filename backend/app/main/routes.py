from random import randint
from flask import request, jsonify, make_response
from . import bp
from .document_manager import DocumentManager


dm = DocumentManager()


@bp.route('/search', methods=['GET'])
def search():
    if request.method == 'GET':
        query = request.args.get('q')
        print(query, flush=True)
        resp = dm.get_random_documents(amount=3)
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
