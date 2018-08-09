import os
from flask import Flask
from flask import jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/', methods=('GET', ))
    def welcome():
        context = {"status": 200, "message": "Welcome to ENOVA!!"}
        return jsonify(context)

    from app.resource import api
    from app.resource import jwt
    jwt.init_app(app)
    api.init_app(app)

    return app
