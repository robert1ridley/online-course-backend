from run import db


class UserDataModelFactory(object):
  def factory(type):
    if type == "STUDENT":
      return UserModelStudent()
    if type == "TEACHER":
      return UserModelTeacher()
    if type == "ADMIN":
      return UserModelAdmin()
    else:
      raise NotImplementedError

  factory = staticmethod(factory)


class UserModelStudent(UserDataModelFactory, db.Model):
  __tablename__ = 'students'

  id = db.Column(db.Integer, primary_key=True)
  uuid = db.Column(db.String(120), unique=True, nullable=False)
  username = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)
  usertype = db.Column(db.String(120), nullable=False)
  is_admin = db.Column(db.Boolean, unique=False, default=False)

  def set_data_fields(self, data):
    self.uuid = data.uuid
    self.username = data.username
    self.password = data.password
    self.is_admin = data.is_admin
    self.usertype = data.usertype

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()
    print(self.id)

  @classmethod
  def find_by_username(cls, username):
    return cls.query.filter_by(username=username).first()

  @classmethod
  def return_all(cls):
    def to_json(json_vals):
      return {
        'username': json_vals.username,
        'password': json_vals.password
      }

    return {'users': list(map(lambda x: to_json(x), UserModelStudent.query.all()))}

  @classmethod
  def delete_all(cls):
    try:
      num_rows_deleted = db.session.query(cls).delete()
      db.session.commit()
      return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
    except:
      return {'message': 'Something went wrong'}


class UserModelTeacher(UserDataModelFactory, db.Model):
  __tablename__ = 'teachers'

  id = db.Column(db.Integer, primary_key=True)
  uuid = db.Column(db.String(120), unique=True, nullable=False)
  username = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)
  usertype = db.Column(db.String(120), nullable=False)
  is_admin = db.Column(db.Boolean, unique=False, default=False)

  def set_data_fields(self, data):
    self.uuid = data.uuid
    self.username = data.username
    self.password = data.password
    self.is_admin = data.is_admin
    self.usertype = data.usertype

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  @classmethod
  def find_by_username(cls, username):
    return cls.query.filter_by(username=username).first()

  @classmethod
  def return_all(cls):
    def to_json(json_vals):
      return {
        'username': json_vals.username,
        'password': json_vals.password
      }

    return {'users': list(map(lambda x: to_json(x), UserModelTeacher.query.all()))}

  @classmethod
  def delete_all(cls):
    try:
      num_rows_deleted = db.session.query(cls).delete()
      db.session.commit()
      return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
    except:
      return {'message': 'Something went wrong'}


class UserModelAdmin(UserDataModelFactory, db.Model):
  __tablename__ = 'admin'

  id = db.Column(db.Integer, primary_key=True)
  uuid = db.Column(db.String(120), unique=True, nullable=False)
  username = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)
  usertype = db.Column(db.String(120), nullable=False)
  is_admin = db.Column(db.Boolean, unique=False, default=False)

  def set_data_fields(self, data):
    self.uuid = data.uuid
    self.username = data.username
    self.password = data.password
    self.is_admin = data.is_admin
    self.usertype = data.usertype

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  @classmethod
  def find_by_username(cls, username):
    return cls.query.filter_by(username=username).first()

  @classmethod
  def return_all(cls):
    def to_json(json_vals):
      return {
        'username': json_vals.username,
        'password': json_vals.password
      }

    return {'users': list(map(lambda x: to_json(x), UserModelAdmin.query.all()))}

  @classmethod
  def delete_all(cls):
    try:
      num_rows_deleted = db.session.query(cls).delete()
      db.session.commit()
      return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
    except:
      return {'message': 'Something went wrong'}


class RevokedTokenModel(db.Model):
  __tablename__ = 'revoked_tokens'
  id = db.Column(db.Integer, primary_key=True)
  jti = db.Column(db.String(120))

  def add(self):
    db.session.add(self)
    db.session.commit()

  @classmethod
  def is_jti_blacklisted(cls, jti):
    query = cls.query.filter_by(jti=jti).first()
    return bool(query)