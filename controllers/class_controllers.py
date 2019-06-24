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
    parser.add_argument('userid', help='id of user')
    parser.add_argument('usertype', help='Enter type: STUDENT | TEACHER | ADMIN')
    parser.add_argument('class_name', help='Enter name of class')
    parser.add_argument('class_description', help='Enter description of class')
    parser.add_argument('end_day', help='Enter end date for class')
    parser.add_argument('end_month', help='Enter end date for class')
    parser.add_argument('end_year', help='Enter end date for class')
    return parser.parse_args()


def get_teacher_data():
    parser.add_argument('userid', help='id of user')
    parser.add_argument('usertype', help='Enter type: STUDENT | TEACHER | ADMIN')
    return parser.parse_args()


def validate_teacher(user):
    usertype = user['usertype']
    if usertype != 'TEACHER' and usertype != 'ADMIN':
        return False, {'error': True, 'message': 'Not Authorized'}
    return True, True


def validate_create_class(data):
    class_name = data['class_name']
    class_description = data['class_description']
    end_day = data['end_day']
    end_month = data['end_month']
    end_year = data['end_year']
    usertype = data['usertype']
    if class_name == '':
        return False, {'error': True, 'message': 'Please fill out Class Name'}
    if class_description == '':
        return False, {'error': True, 'message': 'Please fill out Class Description'}
    if end_day == '' or end_month == '' or end_year == '':
        return False, {'error': True, 'message': 'Please fill out End Date of class'}
    if usertype != 'TEACHER' and usertype != 'ADMIN':
        return False, {'error': True, 'message': 'Not Authorized'}
    return True, True


class CreateNewClassController(Resource):
    @jwt_required
    def post(self):
        class_data = get_create_class_request_data()
        is_valid, payload = validate_create_class(class_data)
        if not is_valid:
            return payload
        usertype = class_data['usertype']
        teacher_id = class_data['userid']
        class_name = class_data['class_name']
        end_day = class_data['end_day']
        end_month = class_data['end_month']
        end_year = class_data['end_year']
        class_description = class_data['class_description']
        class_uuid = generate_uuid()
        created_on = datetime.datetime.utcnow
        username = get_jwt_identity()
        if not UserDataModelFactory.factory(usertype).find_by_username(username):
            return {
                'error': True,
                'message': 'Not valid user {}'.format(username)
            }
        new_class = ClassModel()
        new_class.initiate_resource(teacher_id, username, created_on, class_name)
        now = datetime.datetime.now()
        new_class.created_on = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
        new_class.class_end_date = datetime.datetime(int(end_year), int(end_month), int(end_day), 0, 0, 0)
        new_class.class_uuid = class_uuid
        new_class.class_description = class_description
        class_data_model = ClassDataModel()
        class_data_model.set_data_fields(new_class)
        current_class_name = class_data_model.find_by_class_name(class_name)
        is_already_entity_name = class_data_model.save_to_db()
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


class GetAllTeacherClasses(Resource):
    @jwt_required
    def post(self):
        teacher_data = get_teacher_data()
        teacher_id = teacher_data['userid']
        is_user_valid, payload = validate_teacher(teacher_data)
        if not is_user_valid:
            return payload
        teacher_classes = ClassDataModel.find_by_teacher_id(teacher_id)
        teacher_classlist = []
        for teacher_class in teacher_classes:
            class_ = ClassModel()
            class_.initiate_resource(teacher_class.teacher_id, teacher_class.teacher_name,
                                     teacher_class.created_on, teacher_class.class_name)
            class_.class_uuid = teacher_class.class_uuid
            class_.class_description = teacher_class.class_description
            class_.class_end_date = teacher_class.class_end_date
            class_obj = class_.get_response_object()
            teacher_classlist.append(class_obj)
        print(teacher_classlist)
        # TODO: Figure out way to JSON serialize dates
        return {
            'error': False,
            'message': 'All good',
            # 'classes': teacher_classlist
        }