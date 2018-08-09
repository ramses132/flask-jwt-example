from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)
parser = reqparse.RequestParser()
parser.add_argument(
    'username', help='This field cannot be blank', required=True)
parser.add_argument(
    'password', help='this field cannot be blank', required=True)

USER = {"username": "topitop", "password": "topitop"}

jwt = JWTManager()


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        if data['username'] != USER['username']:
            return {
                "message": "User {} doesn't exist".format(data['username'])
            }

        if data['password'] == USER['password']:
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                "message": "User Logged in as {}".format(data['username']),
                "access_token": access_token,
                "refresh_token": refresh_token
            }

        else:
            return {'message': 'Wrong credentials'}


class TestLogin(Resource):
    @jwt_required
    def get(self):
        return {'status': 200, 'message': "you are logged with JWT"}


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


api = Api(prefix='/api/v1')
api.add_resource(UserLogin, '/login')
api.add_resource(TestLogin, '/test-jwt')
api.add_resource(TokenRefresh, '/token-refresh')
