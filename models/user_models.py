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
    self.is_admin = True
    print("I'm admin")


class UserStudent(UserFactory):
  def __init__(self):
    self.username = None
    self.password = None
    self.id = None
    self.enrolled_courses = []
    self.grades = None
    self.is_admin = False
    print("I'm a student")


class UserTeacher(UserFactory):
  def __init__(self):
    self.username = None
    self.password = None
    self.id = None
    self.courses_teaching = []
    self.is_admin = False
    print("I'm a teacher")