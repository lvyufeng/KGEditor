import json
from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class BaseModel(object):
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

project_partner = db.Table(
    "project_partener",
    db.Column('project_id', db.Integer, db.ForeignKey("project.id"), primary_key=True),
    db.Column('partner_id', db.Integer, db.ForeignKey("user_profile.id"), primary_key=True),
    # authority = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
)

project_graph = db.Table(
    "project_graph",
    db.Column('project_id', db.Integer, db.ForeignKey("project.id"), primary_key=True),
    db.Column('graph_id', db.Integer, db.ForeignKey("graph.id"), primary_key=True),
)

class User(BaseModel, db.Model):
    __tablename__ = 'user_profile'
    id = db.Column(db.Integer, primary_key=True)
    mobile = db.Column(db.String(11), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(32), unique=True, nullable=False)
    graphs = db.relationship('Graph', backref='user_profile')
    # projects = db.relationship('Project', secondary=project_partner)
    
    @property
    def password(self):
        raise AttributeError("Only write")

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
            
class Project(BaseModel, db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey("user_profile.id"), nullable=False)
    name = db.Column(db.String(32), unique=True, nullable=False)
    partners = db.relationship('User', secondary=project_partner)
    # graphs = db.relationship('Graph', secondary=project_graph)
    project_type = db.Column(db.Integer, nullable=False)
    project_status = db.Column(db.Boolean, nullable=False, default=False)
    def to_dict(self):
        return {
            'project_id': self.id,
            'project_name': self.name,
            'project_type': self.project_type,
            'project_status': self.project_status
        }

class Data(BaseModel, db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    data_type = db.Column(db.Integer, nullable=False)
    data_info = db.Column(db.String(500), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey("user_profile.id"), nullable=False)
    private = db.Column(db.Boolean, nullable=False)
    is_raw = db.Column(db.Boolean, nullable=False)
    domain_id = db.Column(db.Integer, db.ForeignKey("domain.id"), nullable=False)
    
    def to_dict(self):
        return {
            'data_name': self.name,
            'data_id': self.id,
            'data_type': self.data_type,
            'private': self.private
        }
    
class Graph(BaseModel, db.Model):
    __tablename__ = 'graph'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey("user_profile.id"), nullable=False)
    private = db.Column(db.Boolean, nullable=False)
    domain_id = db.Column(db.Integer, db.ForeignKey("domain.id"), nullable=False)
    connected = db.Column(db.Boolean, nullable=False, default=False)
    # project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=True)
    def to_dict(self):
        return {
            'graph_id': self.id,
            'graph_name': self.name,
            'private': self.private,
            'domain_id': self.domain_id,
            'connected': self.connected
        }
        
class Domain(BaseModel, db.Model):
    __tablename__ = 'domain'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey("user_profile.id"), nullable=False)

    def to_dict(self):
        return {
            'domain_id': self.id,
            'domain_name': self.name
        }

class Model(BaseModel, db.Model):
    __tablename__ = 'model'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey("user_profile.id"), nullable=False)
    model_type = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(200), unique=True, nullable=False)
    private = db.Column(db.Boolean, nullable=False)
    description = db.Column(db.String(500), nullable=True)

    def to_dict(self):
        return {
            'model_id': self.id,
            'model_name': self.name,
            'model_url': self.url,
            'model_type': self.model_type,
            'model_description': self.description
        }