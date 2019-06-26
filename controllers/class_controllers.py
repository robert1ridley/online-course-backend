import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import datetime
from flask_restful import Resource, reqparse
from data_access_models.user_data_models import UserDataModelFactory
from data_access_models.class_data_models import ClassDataModel, ClassSignupDataModel
from utils import generate_uuid
from models import UserFactory, ClassModel, AssignmentModel, SumbissionModel, SignUpForClassModel
from flask_jwt_extended import (jwt_required, get_jwt_identity)
import json


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


def get_account_type_data():
    parser.add_argument('usertype', help='Enter type: STUDENT | TEACHER | ADMIN')
    return parser.parse_args()


def get_single_class_teacher_req():
    parser.add_argument('userid', help='id of user')
    parser.add_argument('usertype', help='Enter type: STUDENT | TEACHER | ADMIN')
    parser.add_argument('class_id', help='Enter id of class')
    return parser.parse_args()


def sign_up_for_class_data():
    parser.add_argument('userid', help='id of user')
    parser.add_argument('usertype', help='Enter type: STUDENT | TEACHER | ADMIN')
    parser.add_argument('class_id', help='Enter id of class')
    return parser.parse_args()


def get_all_student_class_data():
    parser.add_argument('userid', help='id of user')
    parser.add_argument('usertype', help='Enter type: STUDENT | TEACHER | ADMIN')
    return parser.parse_args()


def validate_teacher(user):
    usertype = user['usertype']
    if usertype != 'TEACHER' and usertype != 'ADMIN':
        return False, {'error': True, 'message': 'Not Authorized'}
    return True, True


def validate_teacher_and_class(teacher_id, class_):
    if teacher_id != class_.teacher_id:
        return False, {'error': True, 'message': 'User not authorized to view resource'}
    return True, True


def convert_date_to_json_serializable(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


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
    if end_day == None or end_month == None or end_year == None:
        return False, {'error': True, 'message': 'Please fill out class finish date'}
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
                'message': 'Class name must be unique'
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
            students_signed_up = ClassSignupDataModel.find_by_class_id(class_.class_uuid)
            if students_signed_up is not None:
                class_.set_students_signed_up(students_signed_up)
            class_obj = class_.get_response_object()
            teacher_classlist.append(class_obj)
        return {
            'error': False,
            'message': 'All good',
            'classes': json.dumps(teacher_classlist, default = convert_date_to_json_serializable)
        }


class GetSingleClassTeacher(Resource):
    @jwt_required
    def post(self):
        request_data = get_single_class_teacher_req()
        class_data_model = ClassDataModel.find_by_class_id(request_data['class_id'])
        if class_data_model is None:
            return {
                'error': True,
                'message': 'Resource not found'
            }
        is_valid, payload = validate_teacher_and_class(request_data['userid'], class_data_model)
        if not is_valid:
            return payload
        else:
            class_ = ClassModel()
            class_.initiate_resource(class_data_model.teacher_id, class_data_model.teacher_name,
                                     class_data_model.created_on, class_data_model.class_name)
            class_.class_uuid = class_data_model.class_uuid
            class_.class_description = class_data_model.class_description
            class_.class_end_date = class_data_model.class_end_date
            class_obj = class_.get_response_object()
            return json.dumps(class_obj, default=convert_date_to_json_serializable)


class GetAllClasses(Resource):
    @jwt_required
    def post(self):
        request_data = get_account_type_data()
        if request_data['usertype'] != 'STUDENT' and request_data['usertype'] != 'ADMIN':
            return {
                'error': True,
                'message': 'Not Authorized to view page'
            }
        all_classes = ClassDataModel.return_all()
        class_list = []
        for c in all_classes['classes']:
            _class = c['json_data']
            class_ = ClassModel()
            class_.initiate_resource(_class.teacher_id, _class.teacher_name,
                                     _class.created_on, _class.class_name)
            class_.class_uuid = _class.class_uuid
            class_.class_description = _class.class_description
            class_.class_end_date = _class.class_end_date
            students_signed_up = ClassSignupDataModel.find_by_class_id(_class.class_uuid)
            if students_signed_up is not None:
                class_.set_students_signed_up(students_signed_up)
            class_obj = class_.get_response_object()
            class_list.append(class_obj)
        return json.dumps(class_list, default=convert_date_to_json_serializable)


class SignUpForClass(Resource):
    @jwt_required
    def post(self):
        request_data = sign_up_for_class_data()
        class_id = request_data['class_id']
        class_data_model = ClassDataModel.find_by_class_id(class_id)
        if class_data_model is None:
            return {
                'error': True,
                'message': 'Resource not found'
            }
        sign_up_model = SignUpForClassModel()
        now = datetime.datetime.now()
        sign_up_model.created_on = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
        sign_up_model.student_id = request_data['userid']
        sign_up_model.class_uuid = request_data['class_id']
        sign_up_model.item_uuid = generate_uuid()
        class_sign_up_data_model = ClassSignupDataModel()
        class_sign_up_data_model.set_data_fields(sign_up_model)
        check_classes = class_sign_up_data_model.find_all_by_student_id(request_data['userid'])
        if check_classes is not None:
            for item in check_classes:
                if item.class_uuid == sign_up_model.class_uuid:
                    return {
                        'error': True,
                        'message': 'You have already signed up for this class'
                    }

        class_sign_up_data_model.save_to_db()
        return {
            'error': False,
            'message': 'Successfully signed up for class'
        }


class GetAllStudentClasses(Resource):
    @jwt_required
    def post(self):
        request_data = get_all_student_class_data()
        student_id = request_data['userid']
        student_classes = ClassSignupDataModel.find_all_by_student_id(student_id)
        if student_classes is None:
            return {
                # TODO: What to return here
                'error': False,
                'message': 'No classes yet'
            }
        classes_signed_up_by_student = []
        for student_class in student_classes:
            class_uuid = student_class.class_uuid
            full_class = ClassDataModel.find_by_class_id(class_uuid)
            full_class_model = ClassModel()
            full_class_model.initiate_resource(full_class.teacher_id, full_class.teacher_name, full_class.created_on, full_class.class_name)
            full_class_model.class_uuid = class_uuid
            full_class_model.class_description = full_class.class_description
            full_class_model.class_end_date = full_class.class_end_date
            students_signed_up = ClassSignupDataModel.find_by_class_id(class_uuid)
            if students_signed_up is not None:
                full_class_model.set_students_signed_up(students_signed_up)
            full_object = full_class_model.get_response_object()
            classes_signed_up_by_student.append(full_object)
        return json.dumps(classes_signed_up_by_student, default=convert_date_to_json_serializable)