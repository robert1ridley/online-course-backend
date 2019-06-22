from models.user_factory import UserFactory

class UserStudent(UserFactory):
  def __init__(self, username, password, id):
    self.username = username
    self.password = password
    self.id = id
    self.enrolled_courses = []
    self.grades = None
    self.is_admin = False