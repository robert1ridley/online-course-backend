import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from flask_restful import Resource, reqparse
from data_access_models.user_data_models import UserDataModelFactory, RevokedTokenModel
from models import UserFactory
from utils import generate_hash, verify_hash, generate_uuid
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

parser = reqparse.RequestParser()
def get_registration_info():
    parser.add_argument('username', help = 'Username field cannot be blank')
    parser.add_argument('password', help = 'Password field cannot be blank')
    parser.add_argument('passwordConfirm', help = 'Password Confirm Should not be blank')
    parser.add_argument('usertype', help='Enter type: STUDENT | TEACHER | ADMIN')
    return parser.parse_args()


def get_usertype():
    parser.add_argument('userid', help='id of user')
    parser.add_argument('usertype', help='Enter type: STUDENT | TEACHER | ADMIN')
    return parser.parse_args()


def validate_register_user(user):
    username = user['username']
    password = user['password']
    pass_confirm = user['passwordConfirm']
    if username == '':
        return False, {'error': True, 'message': 'Username should not be blank'}
    if password == '':
        return False, {'error': True, 'message': 'Password should not be blank'}
    if password != pass_confirm:
        return False, {'error': True, 'message': 'Passwords do not match'}
    return True, True


def validate_login_user(user):
    username = user['username']
    password = user['password']
    if username == '':
        return False, {'error': True, 'message': 'Username should not be blank'}
    if password == '':
        return False, {'error': True, 'message': 'Password should not be blank'}
    return True, True


class UserRegistrationController(Resource):
    def post(self):
        data = get_registration_info()
        is_user_valid, error_message = validate_register_user(data)
        if not is_user_valid:
            return error_message
        user = UserFactory.factory(data['usertype'])
        user.username = data['username']
        user.password = generate_hash(data['password'])
        user.uuid = generate_uuid()
        if UserDataModelFactory.factory(user.usertype).find_by_username(user.username):
            return {
                'error': True,
                'message': 'User {} already exists'.format(user.username)
            }
        new_user = UserDataModelFactory.factory(user.usertype)
        new_user.set_data_fields(user)

        try:
            new_user.save_to_db()
            access_token = create_access_token(identity = user.username)
            refresh_token = create_refresh_token(identity = user.username)
            return {
                'error': False,
                'message': 'User {} was created'.format(user.username),
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user_id': user.uuid
                }
        except:
            return {
                'error': True,
                'message': 'Something went wrong'
                }, 500


class UserLoginController(Resource):
    def post(self):
        data = get_registration_info()
        is_user_valid, error_message = validate_login_user(data)
        if not is_user_valid:
            return error_message
        user = UserFactory.factory(data['usertype'])
        user.username = data['username']
        user.password = data['password']
        current_user = UserDataModelFactory.factory(user.usertype).find_by_username(user.username)
        user.uuid = current_user.uuid
        if not current_user:
            return {
                'error': True,
                'message': 'User {} doesn\'t exist'.format(user.username)
            }

        if verify_hash(user.password, current_user.password):
            access_token = create_access_token(identity = user.username)
            refresh_token = create_refresh_token(identity = user.username)
            return {
                'error': False,
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user_id': user.uuid
                }
        else:
            return {
                'error': True,
                'message': 'Wrong credentials'
            }


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


class SingleStudentUserController(Resource):
    @jwt_required
    def post(self):
        user_data = get_usertype()
        username = get_jwt_identity()
        usertype = user_data['usertype']
        full_user = UserDataModelFactory.factory(usertype).find_by_username(username)
        user = UserFactory.factory(usertype)
        user.username = full_user.username
        user.usertype = full_user.usertype
        user.uuid = full_user.uuid
        user.is_admin = full_user.is_admin
        user_object = user.get_user_object()
        return {
            'error': False,
            'user': user_object
        }


class SingleTeacherUserController(Resource):
    @jwt_required
    def post(self):
        user_data = get_usertype()
        username = get_jwt_identity()
        usertype = user_data['usertype']
        full_user = UserDataModelFactory.factory(usertype).find_by_username(username)
        user = UserFactory.factory(usertype)
        user.username = full_user.username
        user.usertype = full_user.usertype
        user.uuid = full_user.uuid
        user.is_admin = full_user.is_admin
        user_object = user.get_user_object()
        return {
            'error': False,
            'user': user_object
        }


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
