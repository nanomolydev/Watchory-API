from flask import Flask
from flask_smorest import Api
from db import db
import models
from resources.viewing import blp as ViewingBlueprint
from resources.collection import blp as CollectionBlueprint
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['API_TITLE'] = 'Watchory'
    app.config['API_VERSION'] = '1.0.0'
    app.config['OPENAPI_VERSION'] = '3.0.3'

    db.init_app(app)

    api = Api(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(ViewingBlueprint)
    app.register_blueprint(CollectionBlueprint)
    return app