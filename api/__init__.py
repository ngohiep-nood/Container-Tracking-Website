from json import load
from flask import Flask
from api.route.home import home_api
from api.models import db
from dotenv import load_dotenv
from os import path, environ

def create_app():
    app = Flask(__name__)
    url = path.abspath(path.dirname(__name__)) + '/.env'
    load_dotenv(path.normpath(url))
    
    app.config.from_mapping(
        SECRET_KEY= environ.get("SECRET_KEY"),
        SQLALCHEMY_DATABASE_URI=environ.get("SQLALCHEMY_DATABASE_URI"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.app = app
    db.init_app(app)

    app.register_blueprint(home_api)

    return app

