import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import datetime
from flask_restful import Resource, reqparse
from data_access_models.user_data_models import UserDataModelFactory
from data_access_models.class_data_models import ClassDataModel
from utils import generate_uuid
from models import UserFactory, ClassModel, AssignmentModel, SumbissionModel
from flask_jwt_extended import (jwt_required, get_jwt_identity)


parser = reqparse.RequestParser()
def get_create_class_request_data():
    parser.add_argument('userid', help='id of user', required=True)
    parser.add_argument('usertype', help='Enter type: STUDENT | TEACHER | ADMIN', required=True)
    parser.add_argument('class_name', help='Enter name of class', required=True)
    parser.add_argument('class_description', help='Enter description of class', required=True)
    parser.add_argument('end_date', help='Enter end date for class', required=True)
    return parser.parse_args()


class CreateNewClassController(Resource):
    @jwt_required
    def post(self):
        user_data = get_create_class_request_data()
        usertype = user_data['usertype']
        teacher_id = user_data['userid']
        class_name = user_data['class_name']
        end_date = user_data['end_date']
        class_description = user_data['class_description']
        class_uuid = generate_uuid()
        created_on = datetime.datetime.utcnow
        if usertype != 'TEACHER' and usertype != 'ADMIN':
            return {
                'error': True,
                'message': 'not permitted'
            }
        username = get_jwt_identity()
        if not UserDataModelFactory.factory(usertype).find_by_username(username):
            return {
                'error': True,
                'message': 'Not valid user {}'.format(username)
            }
        new_class = ClassModel()
        new_class.initiate_resource(teacher_id, username, created_on, class_name)
        # new_class.class_end_date = end_date
        new_class.class_end_date = datetime.datetime(2012, 3, 3, 10, 10, 10)
        new_class.created_on = datetime.datetime(2012, 3, 3, 10, 10, 10)
        new_class.class_uuid = class_uuid
        new_class.class_description = class_description
        class_data_model = ClassDataModel()
        class_data_model.set_data_fields(new_class)
        current_class_name = class_data_model.find_by_class_name(class_name)
        is_already_entity_name = class_data_model.save_to_db()
        print(current_class_name)
        if current_class_name:
            return {
                'error': True,
                'message': 'Must have unique name'
            }
        if is_already_entity_name:
            return {
                'error': False,
                'message': 'successfully added class'
            }
        return {
            'error': True,
            'message': 'Something went wrong'
        }
