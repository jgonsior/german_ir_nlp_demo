from flask import request, jsonify, make_response, current_app
from random import randint
import torch
import numpy as np
import os

from . import utils
from . import bp

os.environ["CUDA_VISIBLE_DEVICES"] = ""

# Milestone 1
from .document_manager import DocumentManager
dm = DocumentManager()

# Milestone 2
# from app.tf_idf import find_best_results
# qf = find_best_results.queryFinder()

# Milestone 3-5
# check __init__.py
# from .ragatouille_model_manager import RagatouilleModelManager
# model_manager = RagatouilleModelManager()


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
        # k could be passed by the frontend as well?
        k = 100
        results = current_app.rag_model_manager.search(query=query, k=k)
        resp = utils.make_response(results)
        return jsonify(resp)


@bp.route('/word_embeddings', methods=['POST'])
def get_word_embeddings():
    if request.method == 'POST':
        query = request.json['query']
        paragraph = request.json['paragraph']

        words, scores = current_app.rag_model_manager.get_word_scores(query, paragraph, k=3)
        resp = []

        for word, embedding_score in zip(words, scores):
            tmp = {
                'word': word,
                'embedding': embedding_score
            }
            resp.append(tmp)

        return jsonify(resp)


@bp.route('/document', methods=['GET'])
def get_document():
    if request.method == 'GET':
        document_id = request.args.get('id')
        doc = dm.get_document_by_id(document_id)

        print('Get Document id=', document_id)
        if not doc:
                return make_response(jsonify({'error': 'Document not found'}), 404)
        return jsonify(doc)
