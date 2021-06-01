import logging
import pymysql
import json
from flask import abort
from flask import g
from kgeditor.models import Data
from kgeditor import db
from kgeditor.constants import DATA_DB, DATA_DATA, DATA_TEXT

data_dict = {
    'db':DATA_DB,
    'data':DATA_DATA,
    'text':DATA_TEXT
}

class DataDao:
    def __init__(self):
        pass

    def get(self, id):
        pass

    def create(self, data):
        user_id = g.user_id
        if data['data_type'] in ['db', 'text']:
            is_raw = True
        elif data['data_type'] == 'data':
            is_raw = False
        else:
            return abort(400, 'Invalid Parameters.')
        if data['data_type'] == 'db':
            try:
                test_db = pymysql.connect(
                    host = data['data_info']['ip'],
                    port = int(data['data_info']['port']),
                    user = data['data_info']['username'],
                    password = data['data_info']['password'],
                    database = data['data_info']['db']
                )
            except Exception as e:
                logging.error(e)
                return abort(400, 'Invalid parameters.')
            else:
                test_db.close()
        
        data = Data(
            name=data['name'], 
            data_type=data_dict[data['data_type']], 
            creator_id=user_id, 
            private=data['private'], 
            data_info=json.dumps(data['data_info']), 
            is_raw=is_raw,
            domain_id=data['domain_id']
        )
        try:
            db.session.add(data)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return abort(500, 'Database error.')
        
        return {'message':'Create data succeed.'}, 201

    def update(self, id, data):
        pass

    def delete(self, id):
        user_id = g.user_id
        try:
            data = Data.query.filter_by(id=id, creator_id=user_id).first()
        except Exception as e:
            logging.error(e)
            db.session.rollback()
            return abort(500, 'Database error.')
        else:
            if data is None:
                return abort(500, 'Data not exist.')
        try:
            db.session.delete(data)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return abort(500, 'Database error.')
        return {'message':'Delete data succeed.'}, 200
    
    def all(self, dtype):
        if dtype == 'data':
            is_raw = False
        elif dtype == 'text':
            is_raw = True
        else:
            return abort(400, 'Invalid Parameters.')
        user_id = g.user_id
        try:
            data_list = Data.query.filter_by(creator_id=user_id, is_raw=is_raw).all()
        except Exception as e:
            logging.error(e)
            return abort(500, 'Database error.')
        data_dict_list = []
        for data in data_list:
            data_dict_list.append(data.to_dict())
        
        return {'data':data_dict_list, 'message': 'Query data list succeed.'}, 200