from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger

from src.routes.juegos_routes import juegos_bp
from src.routes.editoriales_routes import editoriales_bp
from src.swagger import swagger_config, swagger_template


def create_app():
    app = Flask(__name__)
    CORS(app)

    Swagger(app, config=swagger_config, template=swagger_template)

    app.register_blueprint(juegos_bp)
    app.register_blueprint(editoriales_bp)

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"}), 200
        
    return app
