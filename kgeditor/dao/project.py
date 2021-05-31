import logging
from flask import abort, session, g
from kgeditor.models import Project
from kgeditor import db

class ProjectDAO:
    def __init__(self):
        pass

    def create(self, data):
        user_id = g.user_id
        try:
            project = Project.query.filter_by(name=data['name']).first()
        except Exception as e:
            logging.error(e)
            return abort(500, 'Database error.')
        else:
            if project is not None:
                return abort(500, 'Project already exist.')
        # 5.save graph info to db
        project = Project(name=data['name'], creator_id=user_id, project_type=data['type_id'])
        try:
            db.session.add(project)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return abort(500, 'Database error.')
        return {'message': 'Create project succeed.'}, 201

    def get(self, id):
        user_id = session.get('user_id')
        try:
            project = Project().query.filter_by(id=id, creator_id=user_id).first()
        except Exception as e:
            logging.error(e)
            return abort(500, 'Database error.')
        data = project.to_dict()

        return {'data': data, 'message':'Fetch project succeed.'}, 200

    def update(self, id, data):
        user_id = g.user_id
        try:
            project = Project.query.filter_by(id=id, creator_id=user_id).first()
            project.name = data['name']
        except Exception as e:
            logging.error(e)
            return abort(500, 'Database error.')
        return {'message': 'Update project succeed.'}, 200

    def delete(self, id):
        user_id = session.get('user_id')
        try:
            project = Project.query.filter_by(id=id, creator_id=user_id).first()
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            return abort(500, 'Database error.')
        else:
            if project is None:
                return abort(500, 'Domain not exist.')
        try:
            db.session.delete(project)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return abort(500, 'Database error.')
        return {'message':'Delete project succeed.'}, 200

    def all(self, project_type=None):
        try:
            if project_type is None:
                project_list = Project.query.all()
            else:
                project_list = Project.query.filter_by(project_type=project_type).all()
        except Exception as e:
            logging.error(e)
            return abort(500, 'Database error.')
        project_dict_list = []
        for project in project_list:
            project_dict_list.append(project.to_dict())

        return {'data': project_dict_list, 'message': 'Query succeed.'}, 200