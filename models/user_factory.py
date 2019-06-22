from models.user_student import UserStudent
from models.user_teacher import UserTeacher
from models.user_admin import UserAdmin

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