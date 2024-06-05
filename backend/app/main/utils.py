from flask import current_app
import json
import os

def update_model_metadata():
    index_path = current_app.config.get('INDEX_PATH')
    checkpoint_path = current_app.config.get('CHECKPOINT_PATH')

    metadata_path = os.path.join(index_path, 'metadata.json')

    if not os.path.isfile(metadata_path):
        raise FileNotFoundError("{} does not exist! Check config.ini".format(metadata_path))


    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    metadata['config']['checkpoints'] = checkpoint_path

    with open(metadata_path, 'w') as file:
        json.dump(metadata, file, indent=4)
