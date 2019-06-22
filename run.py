from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'

db = SQLAlchemy(app)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()


app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return user_data_models.RevokedTokenModel.is_jti_blacklisted(jti)

from controllers import user_controllers
from data_access_models import user_data_models

api.add_resource(user_controllers.UserRegistrationController, '/registration')
api.add_resource(user_controllers.UserLoginController, '/login')
api.add_resource(user_controllers.UserLogoutAccessController, '/logout/access')
api.add_resource(user_controllers.UserLogoutRefreshController, '/logout/refresh')
api.add_resource(user_controllers.TokenRefreshController, '/token/refresh')
api.add_resource(user_controllers.AllUsersController, '/users')
api.add_resource(user_controllers.SecretResourceController, '/secret')