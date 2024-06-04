from flask import Flask
from flask_cors import CORS

import configparser
import os

from .main import bp as main_bp
from .tf_idf import bp as tf_idf_bp

app_config = {}

def create_app():
    app = Flask(__name__)
    CORS(app)

    config = configparser.ConfigParser()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(os.path.dirname(base_dir), 'config.ini')

    print(config_path)
    config.read(config_path)

    app.config['INDEX_PATH'] = config.get('paths', 'index')
    app.config['CHECKPOINT_PATH'] = config.get('paths', 'checkpoint')


    app.register_blueprint(main_bp)
    app.register_blueprint(tf_idf_bp)

    return app
