from models.user_factory import UserFactory

class UserAdmin(UserFactory):
  def __init__(self, username, password, id):
    self.username = username
    self.password = password
    self.id = id
    self.is_admin = True