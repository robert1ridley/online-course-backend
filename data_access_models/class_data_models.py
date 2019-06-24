from datetime import datetime
from run import db


class ClassDataModel(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    class_uuid = db.Column(db.String(120), unique=True, nullable=False)
    class_name = db.Column(db.String(120), unique=True, nullable=False)
    class_description = db.Column(db.String(120), unique=False, nullable=False)
    teacher_id = db.Column(db.String(120), unique=False, nullable=False)
    teacher_name = db.Column(db.String(120), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    class_end_date = db.Column(db.DateTime, default=datetime.utcnow)

    def set_data_fields(self, data):
        self.class_uuid = data.class_uuid
        self.class_name = data.class_name
        self.class_description = data.class_description
        self.teacher_id = data.teacher_id
        self.teacher_name = data.teacher_name
        self.created_on = data.created_on
        self.class_end_date = data.class_end_date


    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False


    @classmethod
    def find_by_class_name(cls, class_name):
        return cls.query.filter_by(class_name=class_name).first()


    @classmethod
    def find_by_teacher_id(cls, teacher_id):
        return cls.query.filter_by(teacher_id=teacher_id)


    @classmethod
    def return_all(cls):
        def to_json(json_vals):
            return {
                'json_data': json_vals
            }
        return {'classes': list(map(lambda x: to_json(x), ClassDataModel.query.all()))}


    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}
