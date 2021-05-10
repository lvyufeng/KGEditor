import logging
from flask import request, abort, session
from kgeditor.models import User
from kgeditor import db, redis_store, constants
from sqlalchemy.exc import IntegrityError

class UserDAO:
    def __init__(self):
        pass

    def create(self, data):
        logging.info(data)
        # no need sms code now
        # 1.get sms code from redis
        # 2.verify the sms code outdate time
        # 3.verify the sms code
        # 4.verify whether the phone number already registered
        try:
            user = User.query.filter_by(mobile=data['mobile']).first()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return abort(500, 'Database error.')
        else:
            if user is not None:
                return abort(500, 'Phone number already exist.')
        # 5.save user info to db
        user = User(mobile=data['mobile'], name=data['name'])
        user.password = data['password']
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            # phone number duplicate
            logging.error(e)
            return abort(500, 'User name already exist.')
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return abort(500, 'Database error.')
        return {'message': 'Register succeed.'}, 201

    def get(self, data):
        user_ip = request.remote_addr
        logging.info(user_ip)
        try:
            access_nums = redis_store.get("access_nums_%s" % user_ip)
        except Exception as e:
            logging.error(e)
        else:
            if access_nums is not None and int(access_nums) >= constants.LOGIN_ERROR_MAX_TIMES:
                return abort(405, 'Too many times.') 
        # fetch user by phone number
        try:
            user = User.query.filter_by(mobile=data['mobile']).first()
        except Exception as e:
            logging.error(e)
            return abort(500, 'Fetch user information failed.')

        # verify password
        # if login failed, record failed times
        if user is None or not user.check_password(data['password']):
            try:
                redis_store.incr("access_nums_%s" % user_ip)
                redis_store.expire("access_nums_%s" % user_ip, constants.LOGIN_ERROR_FORBID_TIME)
            except Exception as e:
                logging.error(e)
            return abort(400, 'Wrong username or password')
        session['name'] = user.name
        session['user_id'] = user.id
        return {'message': 'Login succeed.'}, 200
