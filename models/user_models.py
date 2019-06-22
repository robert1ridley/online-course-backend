class UserFactory(object):

  def factory(type):
    if type == "STUDENT":
      return UserStudent()
    if type == "TEACHER":
      return UserTeacher()
    if type == "ADMIN":
      return UserAdmin()
    else:
      raise NotImplementedError

  factory = staticmethod(factory)


class UserAdmin(UserFactory):
  def __init__(self):
    self.username = None
    self.password = None
    self.id = None
    self.usertype = 'ADMIN'
    self.is_admin = True


class UserStudent(UserFactory):
  def __init__(self):
    self.username = None
    self.password = None
    self.id = None
    self.usertype = 'STUDENT'
    self.is_admin = False
    self.classes_signed_up = []
    self.grades = {}


class UserTeacher(UserFactory):
  def __init__(self):
    self.username = None
    self.password = None
    self.id = None
    self.usertype = 'TEACHER'
    self.is_admin = False
    self.teaching_classes = []