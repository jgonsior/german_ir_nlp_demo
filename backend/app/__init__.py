from flask import Flask
from .main import bp as main_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_bp)

    return app
    

