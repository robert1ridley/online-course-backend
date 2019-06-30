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
    self.uuid = None
    self.usertype = 'ADMIN'
    self.is_admin = True


class UserStudent(UserFactory):
  def __init__(self):
    self.username = None
    self.password = None
    self.uuid = None
    self.usertype = 'STUDENT'
    self.is_admin = False


  def get_user_object(self):
    user = {
      'username': self.username,
      'uuid': self.uuid,
      'usertype': self.usertype,
      'is_admin': self.is_admin
    }

    return user


class UserTeacher(UserFactory):
  def __init__(self):
    self.username = None
    self.password = None
    self.uuid = None
    self.usertype = 'TEACHER'
    self.is_admin = False


  def get_user_object(self):
    user = {
      'username': self.username,
      'uuid': self.uuid,
      'usertype': self.usertype,
      'is_admin': self.is_admin
    }

    return user
