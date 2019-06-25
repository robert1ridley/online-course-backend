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
        self.teacher_id = None
        self.assignment_content = None
        self.created_on = None
        self.deadline = None
        self.submissions = []

    def set_teacher_id(self, teacher_id):
        self.teacher_id = teacher_id

    def set_created_on(self, created_on):
        self.created_on = created_on

    def set_class_name(self, class_name):
        self.class_name = class_name


class SumbissionModel(ResourseInfo):
    def __init__(self):
        self.submission_id = None
        self.class_name = None
        self.created_on = None
        self.teacher_id = None
        self.student_id = None
        self.grade = None
        self.content = None
        self.comments = None

    def set_teacher_id(self, teacher_id):
        self.teacher_id = teacher_id

    def set_created_on(self, created_on):
        self.created_on = created_on

    def set_class_name(self, class_name):
        self.class_name = class_name


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
