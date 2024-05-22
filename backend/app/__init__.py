from flask import Flask
from flask_cors import CORS

from .main import bp as main_bp
#from .tf_idf import bp as tf_idf_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(main_bp)
    #app.register_blueprint(tf_idf_bp)

    return app
    

