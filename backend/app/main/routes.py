from flask import request, jsonify, make_response, current_app
from random import randint
import torch
import numpy as np
import os

from .ragatouille_model_manager import RagatouilleModelManager
from . import utils
from . import bp

os.environ["CUDA_VISIBLE_DEVICES"] = ""

# Milestone 1
# from .document_manager import DocumentManager
# dm = DocumentManager()

# Milestone 2
# from app.tf_idf import find_best_results
# qf = find_best_results.queryFinder()

# Milestone 3-5
model_manager = RagatouilleModelManager()


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
        k = 5
        results = model_manager.search(query=query, k=k)
        query_embeddings = model_manager.get_query_embeddings(query)
        document_embeddings = model_manager.get_document_embeddings(results)

        print('------------------------------------------')
        print(results)
        print('------------------------------------------')

        utils.reformat_response(results, query_embeddings, document_embeddings)

        print('Length query embeddings ', str(len(query_embeddings[0])))
        #print(np.array(query_embeddings).shape)
        print('Length document embeddings ', str(len(document_embeddings)))
        #print(np.array(document_embeddings).shape)
        print('Length first document embeddings ', str(len(document_embeddings[0])))

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
