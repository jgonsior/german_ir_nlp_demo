from flask import Flask
from flask_cors import CORS

import configparser
import os


def create_app():
    app = Flask(__name__)
    CORS(app)


    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.ini')

    config = configparser.ConfigParser()
    config.read(config_path)

    app.config['INDEX_PATH'] = os.path.join(os.path.abspath(os.path.join(app.root_path, os.pardir)), config.get('paths', 'index'))
    app.config['CHECKPOINT_PATH'] = os.path.join(os.path.abspath(os.path.join(app.root_path, os.pardir)), config.get('paths', 'checkpoint'))


    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    # Milestone 2
    #from .tf_idf import bp as tf_idf_bp
    #app.register_blueprint(tf_idf_bp)

    return app
