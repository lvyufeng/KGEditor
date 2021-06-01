import logging
from flask import abort, session, g
from kgeditor.models import Model
from kgeditor import db

class ModelDAO:
    def __init__(self):
        pass

    def create(self, data):
        user_id = g.user_id
        try:
            domain = Model.query.filter_by(name=data['model_name']).first()
        except Exception as e:
            logging.error(e)
            return abort(500, 'Database error.')
        else:
            if domain is not None:
                return abort(500, 'Model already exist.')

        model = Model(name=data.get('model_name'), creator_id=user_id, model_type=data.get('model_type'), url=data.get('model_url'), private=data.get('model_private'), description=data.get('model_description', None))
        try:
            db.session.add(model)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return abort(500, 'Database error.')
        
        return {'message': 'Create model succeed.'}, 201

    def get(self, id):
        user_id = session.get('user_id')
        try:
            model = Model.query.filter_by(id=id, creator_id=user_id).first()
        except Exception as e:
            logging.error(e)
            return abort(500, 'Database error.')
        else:
            if not model:
                return abort(500, 'Model not exist.')
        data = model.to_dict()

        return {'data': data, 'message':'Fetch model succeed.'}, 200

    def update(self, id, data):
        logging.info(data)
        try:
            model = Model.query.filter_by(id=id).first()
            model.name = data['model_name']
            model.model_type = data['model_type']
            model.url = data['model_url']
            # model.private = data['model_private']
            model.description = data.get('model_description')
            db.session.commit()
        except Exception as e:
            logging.error(e)
            return abort(500, 'Database error.')
        return {'message':'Update model succeed'}, 200

    def delete(self, id):
        user_id = session.get('user_id')
        try:
            model = Model.query.filter_by(id=id, creator_id=user_id).first()
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            return abort(500, 'Database error.')
        else:
            if model is None:
                return abort(500, 'Domain not exist.')
        try:
            db.session.delete(model)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return abort(500, 'Database error.')
        return {'message':'Delete model succeed.'}, 200

    def all(self, model_type=None):
        try:
            if model_type is None:
                model_list = Model.query.all()
            else:
                model_list = Model.query.filter_by(model_type=model_type).all()
        except Exception as e:
            logging.error(e)
            return abort(500, 'Database error.')
        model_dict_list = []
        for model in model_list:
            model_dict_list.append(model.to_dict())

        return {'data': model_dict_list, 'message': 'Query succeed.'}, 200