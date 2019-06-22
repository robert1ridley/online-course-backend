from models.user_factory import UserFactory

class UserTeacher(UserFactory):
  def __init__(self, username, password, id):
    self.username = username
    self.password = password
    self.id = id
    self.courses_teaching = []
    self.is_admin = False