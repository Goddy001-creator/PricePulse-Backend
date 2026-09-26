from flask import Flask, jsonify
from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    CORS(app)

    from app.api.health import health_bp
    from app.api.products import products_bp
    from app.api.scraper import scraper_bp
    from app.api.analytics import analytics_bp

    app.register_blueprint(
        health_bp,
        url_prefix="/api"
    )

    app.register_blueprint(
        products_bp,
        url_prefix="/api"
    )

    app.register_blueprint(
        scraper_bp,
        url_prefix="/api"
    )

    app.register_blueprint(
        analytics_bp,
        url_prefix="/api"
    )

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Endpoint not found"
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "error": "Internal server error"
        }), 500

    return app
