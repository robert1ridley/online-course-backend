import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from data_access_models.user_data_models import UserDataModelFactory
from models import UserFactory
import types

class ResourseInfo:
    """Template pattern for class(课程) and assignment classes"""

    def set_teacher_id(self, teacher_id): pass
    def set_created_on(self, created_on): pass
    def set_class_name(self, class_name): pass
    def set_teacher_name(self, teacher_name): pass


    def initiate_resource(self, teacher_id, teacher_name, created_on, class_name):
        self.set_teacher_id(teacher_id)
        self.set_created_on(created_on)
        self.set_class_name(class_name)
        self.set_teacher_name(teacher_name)


class ClassModel(ResourseInfo):
    def __init__(self):
        self.class_uuid = None
        self.class_name = None
        self.class_description = None
        self.teacher_id = None
        self.teacher_name = None
        self.created_on = None
        self.class_end_date = None
        self.students_signed_up = []
        self.assignments = []

    def set_teacher_id(self, teacher_id):
        self.teacher_id = teacher_id

    def set_created_on(self, created_on):
        self.created_on = created_on

    def set_class_name(self, class_name):
        self.class_name = class_name

    def set_teacher_name(self, teacher_name):
        self.teacher_name = teacher_name

    def set_class_description(self, class_description):
        self.class_description = class_description

    def set_students_signed_up(self, students_signed_up):
        """Accept students_signed_up as instance of ClassSignupDataModel"""
        for s in students_signed_up:
            student_id = s.student_id
            student = UserDataModelFactory.factory('STUDENT')
            student_data_obj = student.find_by_uuid(student_id)
            student_model = UserFactory.factory('STUDENT')
            student_model.username = student_data_obj.username
            student_model.uuid = student_data_obj.uuid
            student_model.usertype = student_data_obj.usertype
            student_model.is_admin = student_data_obj.is_admin
            student_object = student_model.get_user_object()
            self.students_signed_up.append(student_object)

    def set_assignments(self, assignments):
        """Accept assignments as instance of AssignmentDataModel"""
        for ass in assignments:
            assignment = AssignmentModel()
            assignment.initiate_resource(ass.teacher_id, ass.teacher_name, ass.created_on, ass.class_name)
            assignment.assignment_id = ass.assignment_uuid
            assignment.class_id = ass.class_uuid
            assignment.assignment_title = ass.assignment_title
            assignment.assignment_content = ass.assignment_content
            assignment.deadline = ass.deadline
            assignment_object = assignment.get_response_object()
            self.assignments.append(assignment_object)


    def get_response_object(self):
        class_ = {
            'class_uuid': self.class_uuid,
            'class_name': self.class_name,
            'class_description': self.class_description,
            'teacher_id': self.teacher_id,
            'teacher_name': self.teacher_name,
            'created_on': self.created_on,
            'class_end_date': self.class_end_date,
            'students_signed_up': self.students_signed_up,
            'assignments': self.assignments
        }
        return class_


class AssignmentModel(ResourseInfo):
    def __init__(self):
        self.assignment_id = None
        self.class_name = None
        self.class_id = None
        self.teacher_id = None
        self.teacher_name = None
        self.assignment_title = None
        self.assignment_content = None
        self.created_on = None
        self.deadline = None
        self.submissions = None

    def set_teacher_id(self, teacher_id):
        self.teacher_id = teacher_id

    def set_teacher_name(self, teacher_name):
        self.teacher_name = teacher_name

    def set_created_on(self, created_on):
        self.created_on = created_on

    def set_class_name(self, class_name):
        self.class_name = class_name

    def set_assignment_submissions_student(self):
        self.submissions = {}

    def set_assignment_submissions_teacher(self):
        self.submissions = []

    def get_response_object(self):
        assignment = {
            'assignment_id': self.assignment_id,
            'class_name': self.class_name,
            'class_id': self.class_id,
            'teacher_id': self.teacher_id,
            'teacher_name': self.teacher_name,
            'assignment_title': self.assignment_title,
            'assignment_content': self.assignment_content,
            'created_on': self.created_on,
            'deadline': self.deadline,
            'submissions': self.submissions
        }
        return assignment


class SubmissionModel(ResourseInfo):
    def __init__(self):
        self.submission_id = None
        self.assignment_id = None
        self.class_id = None
        self.class_name = None
        self.created_on = None
        self.teacher_id = None
        self.teacher_name = None
        self.student_id = None
        self.student_name = None
        self.grade = None
        self.content = None

    def set_teacher_id(self, teacher_id):
        self.teacher_id = teacher_id

    def set_teacher_name(self, teacher_name):
        self.teacher_name = teacher_name

    def set_created_on(self, created_on):
        self.created_on = created_on

    def set_class_name(self, class_name):
        self.class_name = class_name

    def get_response_object(self):
        submission = {
            'submission_id': self.submission_id,
            'assignment_id': self.assignment_id,
            'class_id': self.class_id,
            'class_name': self.class_name,
            'created_on': self.created_on,
            'teacher_id': self.teacher_id,
            'teacher_name': self.teacher_name,
            'student_id': self.student_id,
            'student_name': self.student_name,
            'grade': self.grade,
            'content': self.content
        }

        return submission

class SignUpForClassModel(ResourseInfo):
    def __init__(self):
        self.item_uuid = None
        self.class_uuid = None
        self.student_id = None
        self.created_on = None


    def get_response_object(self):
        signup_object = {
            'item_uuid': self.item_uuid,
            'class_uuid': self.class_uuid,
            'student_id': self.student_id,
            'created_on': self.created_on
        }

        return signup_object
