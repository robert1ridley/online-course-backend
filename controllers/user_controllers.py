import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from flask_restful import Resource, reqparse
from data_access_models.user_data_models import UserDataModelFactory, RevokedTokenModel
from models import UserFactory
from utils import generate_hash, verify_hash
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)


parser = reqparse.RequestParser()
def get_registration_info():
    parser.add_argument('username', help = 'This field cannot be blank', required = True)
    parser.add_argument('password', help = 'This field cannot be blank', required = True)
    parser.add_argument('usertype', help = 'Enter type: STUDENT | TEACHER | ADMIN', required = True)
    return parser.parse_args()

def get_usertype():
    parser.add_argument('usertype', help='Enter type: STUDENT | TEACHER | ADMIN', required=True)
    return parser.parse_args()


class UserRegistrationController(Resource):
    def post(self):
        data = get_registration_info()
        user = UserFactory.factory(data['usertype'])
        user.username = data['username']
        user.password = generate_hash(data['password'])
        if UserDataModelFactory.factory(user.usertype).find_by_username(user.username):
            return {'message': 'User {} already exists'.format(user.username)}
        new_user = UserDataModelFactory.factory(user.usertype)
        new_user.set_data_fields(user)

        try:
            new_user.save_to_db()
            access_token = create_access_token(identity = user.username)
            refresh_token = create_refresh_token(identity = user.username)
            return {
                'message': 'User {} was created'.format(user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        except:
            return {'message': 'Something went wrong'}, 500


class UserLoginController(Resource):
    def post(self):
        data = get_registration_info()
        user = UserFactory.factory(data['usertype'])
        user.username = data['username']
        user.password = data['password']
        current_user = UserDataModelFactory.factory(user.usertype).find_by_username(user.username)

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(user.username)}

        if verify_hash(user.password, current_user.password):
            access_token = create_access_token(identity = user.username)
            refresh_token = create_refresh_token(identity = user.username)
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        else:
            return {'message': 'Wrong credentials'}


class UserLogoutAccessController(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefreshController(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefreshController(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}


class AllUsersController(Resource):
    def get(self):
        user_data = get_usertype()
        usertype = user_data['usertype']
        return UserDataModelFactory.factory(usertype).return_all()

    def delete(self):
        user_data = get_usertype()
        usertype = user_data['usertype']
        return UserDataModelFactory.factory(usertype).delete_all()


class SecretResourceController(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }
