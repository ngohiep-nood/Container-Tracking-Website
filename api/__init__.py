from flask import Flask
from api.route.home import home_api
from api.route.auth import auth
from api.models import db
from dotenv import load_dotenv
from os import path, environ
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    url = path.abspath(path.dirname(__name__)) + '/.env'
    load_dotenv(path.normpath(url))
    
    app.config.from_mapping(
        SECRET_KEY=environ.get("SECRET_KEY"),
        SQLALCHEMY_DATABASE_URI=environ.get("SQLALCHEMY_DATABASE_URI"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY=environ.get("JWT_SECRET_KEY")
    )
    
    jwt = JWTManager(app)
    db.app = app
    db.init_app(app)

    @app.route('/', methods=['GET'])
    def welcome():
        return '<h1>🚀Welcome to container tracking website!🚀</h1>'

    app.register_blueprint(home_api)
    app.register_blueprint(auth)

    return app

