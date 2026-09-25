from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    CORS(app)

    from app.api.health import health_bp
    app.register_blueprint(health_bp, url_prefix="/api")

    return app
