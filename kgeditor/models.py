from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class BaseModel(object):
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class User(BaseModel, db.Model):
    __tablename__ = 'user_profile'
    id = db.Column(db.Integer, primary_key=True)
    mobile = db.Column(db.String(11), unique=True, nullable=False)
    passwor_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(32), unique=True, nullable=False)
    # graphs = db.relationship('Graph', backref='user')
    
    @property
    def password(self):
        raise AttributeError("Only write")

    @password.setter
    def password(self, value):
        self.passwor_hash = generate_password_hash(value)

    def check_password(self, password):
        return check_password_hash(self.passwor_hash, password)
            
# class Project(BaseModel, db.Model):
#     pass

# class DataBase(BaseModel, db.Model):
#     pass

# class Model(BaseModel, db.Model):
#     pass

# class Graph(BaseModel, db.Model):
#     pass


    