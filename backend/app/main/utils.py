from flask import current_app
import json
import os

def update_model_metadata():
    #index_path = current_app.config.get('INDEX_PATH')
    index_path = "/home/jsiebel/uni/semester/semester10/forschungsprojekt_db/german_ir_nlp_demo/backend//data/colbert/indexes/bert-base-german-cased/GermanDPR-XQA-HP/epoch1"

    # checkpoint_path = current_app.config.get('CHECKPOINT_PATH')
    checkpoint_path = "/home/jsiebel/uni/semester/semester10/forschungsprojekt_db/german_ir_nlp_demo/backend/data/colbert/checkpoints/bert-base-german-cased/GermanDPR-XQA-HP/epoch1"

    metadata_path = os.path.join(index_path, 'metadata.json')

    if not os.path.isfile(metadata_path):
        raise FileNotFoundError("{} does not exist! Check config.ini".format(metadata_path))


    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    metadata['config']['checkpoints'] = checkpoint_path

    with open(metadata_path, 'w') as file:
        json.dump(metadata, file, indent=4)



def reformat_response(results, query_embeddings, document_embeddings):

    query_embeddings_list = query_embeddings.tolist()

    for i, result in enumerate(results):
        result['query_embeddings'] = query_embeddings_list
        result['document_embeddings'] = document_embeddings[i].tolist()
