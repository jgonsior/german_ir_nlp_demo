from flask import request, jsonify, make_response, current_app
from ragatouille import RAGPretrainedModel
from random import randint
import torch
import os


from . import bp
from . import utils

os.environ["CUDA_VISIBLE_DEVICES"] = ""

# Milestone 1
# from .document_manager import DocumentManager
# dm = DocumentManager()

# Milestone 2
# from app.tf_idf import find_best_results
# qf = find_best_results.queryFinder()

# Milestone 3-5
MODEL_RAG = None

@bp.before_app_request
def initialize_model():
    global MODEL_RAG
    # Update metadata.json (checkpoint path)
    utils.update_model_metadata()
    INDEX_PATH = current_app.config.get('INDEX_PATH')
    MODEL_RAG = RAGPretrainedModel.from_index(INDEX_PATH)


@bp.route('/search', methods=['GET'])
def search():
    if request.method == 'GET':
        query = request.args.get('q')
        print(query, flush=True)

        # Milestone 1
        # resp = dm.get_random_documents(amount=3)

        # Milestone 2
        # resp = qf.query_vector_finder(query, 3)

        # Milestone 3-5
        k = 5
        results = MODEL_RAG.search(query=query, k=k)

        print('------------------------------------------')
        print(results)
        print('------------------------------------------')

        return jsonify(results)


@bp.route('/document/', methods=['GET'])
def get_document():
    if request.method == 'GET':
        document_id = request.args.get('id')
        doc = dm.get_document_by_id(document_id)
        print('Get Document id=', document_id)
        if not doc:
                return make_response(jsonify({'error': 'Document not found'}), 404)
        return jsonify(doc)
