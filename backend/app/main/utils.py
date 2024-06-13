from flask import current_app
import json
import os
import re

from .document_manager import DocumentManager
dm = DocumentManager()

def update_model_metadata(index_path, checkpoint_path):

    metadata_path = os.path.join(index_path, 'metadata.json')

    if not os.path.isfile(metadata_path):
        raise FileNotFoundError("{} does not exist! Check config.ini".format(metadata_path))


    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    metadata['config']['checkpoint'] = checkpoint_path

    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=4)


def make_response(results):
    seen_ids = set()
    unique_results = []

    for i, result in enumerate(results):
        # rename fields for frontend
        doc_id = result.pop('document_id').split('-')[0]
        result['id'] = doc_id

        # Skip duplicate ids
        if doc_id in seen_ids:
            continue
        seen_ids.add(doc_id)

        # replace bracket part if passage starts with [
        pattern = r'^\[.*?\]'
        # replace with empty string and rename field from content to passage
        result['passage'] = re.sub(pattern, '', result.pop('content')).strip()

        del result['passage_id']

        doc = dm.get_document_by_id(doc_id)
        result['title'] = doc['title']

        unique_results.append(result)

    return unique_results
