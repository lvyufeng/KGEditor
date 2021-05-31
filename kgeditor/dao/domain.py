import logging
from flask import session, abort
from kgeditor import db
from kgeditor.models import Domain

class DomainDAO:
    def __init__(self):
        pass

    def get(self, id):
        user_id = session.get('user_id')
        try:
            domain = Domain.query.filter_by(id=id, creator_id=user_id).first()
        except Exception as e:
            logging.error(e)
            return abort(500, 'Database error.')
        data = domain.to_dict()

        return {'data': data, 'message':'Fetch domain succeed.'}, 200

    def create(self, data):
        user_id = session.get('user_id')
        logging.info(data)
        try:
            domain = Domain.query.filter_by(name=data['name']).first()
        except Exception as e:
            logging.error(e)
            return abort(500, 'Database error.')
        else:
            if domain is not None:
                return abort(500, 'Domain already exist.')

        domain = Domain(name=data['name'], creator_id=user_id)
        try:
            db.session.add(domain)
            db.session.commit()
            # arango_conn.createDatabase(name="domain_{}".format(domain.id))
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return abort(500, 'Database error.')

        return {'message': 'Create domain succeed.'}, 201

    def update(self, id, data):
        user_id = session.get('user_id')
        try:
            domain = Domain.query.filter_by(id=id, creator_id=user_id).first()
            domain.name = data['name']
            db.session.commit()
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            return abort(500, 'Database error.')

        return {'message': 'Updata domain succeed.'}, 200

    def delete(self, id):
        user_id = session.get('user_id')
        try:
            domain = Domain.query.filter_by(id=id, creator_id=user_id).first()
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            return abort(500, 'Database error.')
        else:
            if domain is None:
                return abort(500, 'Domain not exist.')
        try:
            db.session.delete(domain)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return abort(500, 'Database error.')
        return {'message':'Delete domain succeed.'}, 200

    @property
    def all(self):
        try:
            domain_list = Domain.query.all()
        except Exception as e:
            logging.error(e)
            return abort(500, 'Database error.')
        domain_dict_list = []
        for domain in domain_list:
            domain_dict_list.append(domain.to_dict())

        return {'data': domain_dict_list, 'message': 'Query succeed.'}, 200