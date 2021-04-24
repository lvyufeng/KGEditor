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
        logging.info(data)
        return []