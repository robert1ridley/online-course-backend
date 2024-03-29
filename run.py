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
app.config['PROPAGATE_EXCEPTIONS'] = True
jwt = JWTManager(app)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return user_data_models.RevokedTokenModel.is_jti_blacklisted(jti)

from controllers import user_controllers, class_controllers
from data_access_models import user_data_models

api.add_resource(user_controllers.UserRegistrationController, '/registration')
api.add_resource(user_controllers.UserLoginController, '/login')
api.add_resource(user_controllers.UserLogoutAccessController, '/logout/access')
api.add_resource(user_controllers.UserLogoutRefreshController, '/logout/refresh')
api.add_resource(user_controllers.TokenRefreshController, '/token/refresh')
api.add_resource(user_controllers.SingleStudentUserController, '/user/student')
api.add_resource(user_controllers.SingleTeacherUserController, '/user/teacher')
api.add_resource(user_controllers.AllUsersController, '/users')
api.add_resource(user_controllers.SecretResourceController, '/secret')
api.add_resource(class_controllers.CreateNewClassController, '/user/teacher/newclass')
api.add_resource(class_controllers.GetAllTeacherClasses, '/user/teacher/allclasses')
api.add_resource(class_controllers.GetSingleClassTeacher, '/user/teacher/singleclass')
api.add_resource(class_controllers.GetAllClasses, '/user/student/allclasses')
api.add_resource(class_controllers.GetSingleClassStudent, '/user/student/singleclass')
api.add_resource(class_controllers.SignUpForClass, '/user/student/classsignup')
api.add_resource(class_controllers.GetAllStudentClasses, '/user/student/myclasses')
api.add_resource(class_controllers.AddAssignment, '/user/teacher/newassignment')
api.add_resource(class_controllers.GetSingleAssignmentTeacher, '/user/teacher/assignment/retrieve')
api.add_resource(class_controllers.GetSingleAssignmentStudent, '/user/student/assignment/retrieve')
api.add_resource(class_controllers.SetSubmission, '/user/student/assignment/submit')
api.add_resource(class_controllers.SetAssignmentGrade, '/user/teacher/assignment/grade')
