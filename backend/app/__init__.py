from flask import Flask
from flask_cors import CORS

import configparser
import os

from app.main.ragatouille_model_manager import create_ragatouille_model_manager


def create_app():
    app = Flask(__name__)
    CORS(app)


    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.ini')

    config = configparser.ConfigParser()
    config.read(config_path)

    index_path = os.path.join(os.path.abspath(os.path.join(app.root_path, os.pardir)), config.get('paths', 'index'))
    app.config['INDEX_PATH'] = index_path

    checkpoint_path = os.path.join(os.path.abspath(os.path.join(app.root_path, os.pardir)), config.get('paths', 'checkpoint'))
    app.config['CHECKPOINT_PATH'] = checkpoint_path
    app.config['CORS_HEADERS'] = 'Content-Type'


    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    # Milestone 3-5
    with app.app_context():
        app.rag_model_manager = create_ragatouille_model_manager(index_path, checkpoint_path)

    # Milestone 2
    #from .tf_idf import bp as tf_idf_bp
    #app.register_blueprint(tf_idf_bp)

    return app
