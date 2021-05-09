import re
import logging
from flask import request, jsonify, session
from kgeditor.utils.response_code import RET
from kgeditor.models import User
from kgeditor import db, redis_store, constants
from sqlalchemy.exc import IntegrityError

class UserDAO:
    def __init__(self):
        pass

    def create(self, data):
        try:
            user = User.query.filter_by(mobile=mobile).first()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return jsonify(errno=RET.DBERR, errmsg='数据库异常')
        else:
            if user is not None:
                return jsonify(errno=RET.DATAEXIST, errmsg='手机号已存在')
            logging.info(data)
        return []