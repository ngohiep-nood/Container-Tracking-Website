from flask import Flask, jsonify
from src.route.home import home_api
from src.route.auth import auth
from src.route.admin import admin
from src.models import db
from dotenv import load_dotenv
from os import path, environ
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from src.config.swagger import template, swagger_config

def create_app():
    app = Flask(__name__)
    url = path.abspath(path.dirname(__name__)) + '/.env'
    load_dotenv(path.normpath(url))

    app.config.from_mapping(
        SECRET_KEY=environ.get("SECRET_KEY"),
        SQLALCHEMY_DATABASE_URI=environ.get("SQLALCHEMY_DATABASE_URI"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=environ.get("JWT_SECRET_KEY"),

        SWAGGER={
            'title': "Container Tracking API",
            'uiversion': 3,
            # 'openapi': '3.0.2'
        }
    )

    Swagger(app, template=template, config=swagger_config)

    jwt = JWTManager(app)
    db.app = app
    db.init_app(app)
    
    app.register_blueprint(home_api)
    app.register_blueprint(auth)
    app.register_blueprint(admin)

    @app.errorhandler(404)
    def handle_not_found(e):
        return jsonify({'status': 'error', 'message': 'Not found'}), 404

    @app.errorhandler(500)
    def handle_internal_err(e):
        return jsonify({'status': 'error', 'message': 'Internal Error'}), 500

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({'status': 'error', 'message': 'you used wrong request method'})

    return app


app = create_app()
