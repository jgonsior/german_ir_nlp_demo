from flask import current_app
import json
import os

from .document_manager import DocumentManager
dm = DocumentManager()

def update_model_metadata(index_path, checkpoint_path):

    metadata_path = os.path.join(index_path, 'metadata.json')

    if not os.path.isfile(metadata_path):
        raise FileNotFoundError("{} does not exist! Check config.ini".format(metadata_path))


    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    metadata['config']['checkpoint'] = checkpoint_path

    with open(metadata_path, 'w') as file:
        json.dump(metadata, file, indent=4)


def rename_fields_and_add_title(results):

    for i, result in enumerate(results):
        # rename fields for frontend
        doc_id = result.pop('document_id').split('-')[0]
        result['id'] = doc_id
        result['passage'] = result.pop('content')

        del result['passage_id']

        doc = dm.get_document_by_id(doc_id)
        result['title'] = doc['title']

    print(results)
