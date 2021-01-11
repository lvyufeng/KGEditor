import re
import logging
from . import api
from flask import request, jsonify, session
from kgeditor.utils.response_code import RET
from kgeditor.models import User
from kgeditor import db, redis_store, constants
from sqlalchemy.exc import IntegrityError

@api.route('/users', methods=['post'])
def register():
    """
    register user
    """
    # get request json, return dict
    req_dict = request.get_json()
    mobile = req_dict.get('mobile')
    name = req_dict.get('name')
    password = req_dict.get('password')
    password2 = req_dict.get('password2')
    # verify
    if not all([mobile, password]):
        return jsonify(errno=RET.PRAMERR, errmsg="参数不完整")

    # phone number format
    if not re.match(r'1[34578]\d{9}', mobile):
        # wrong format
        return jsonify(errno=RET.PARAMERR, errmsg="手机号码格式错误")

    if password != password2:
        return jsonify(errno=RET.PARAMERR, errmsg="输入密码不一致")

    # no need sms code now
    # 1.get sms code from redis
    # 2.verify the sms code outdate time
    # 3.verify the sms code
    # 4.verify whether the phone number already registered
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    else:
        if user is not None:
            return jsonify(errno=RET.DATAEXIST, errmsg='手机号已存在')
    # 5.save user info to db
    user = User(mobile=mobile, name=name)
    user.password = password
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        # phone number duplicate
        logging.error(e)
        return jsonify(errno=RET.DATAEXIST, errmsg='手机号已存在')
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据库异常')
    # 6.save login status to session
    session['name'] = name
    session['mobile'] = mobile
    session['user_id'] = user.id
    # 7.return result
    return jsonify(errno=RET.OK, errmsg="注册成功")


@api.route("/session", methods=['POST'])
def login():
    """
    user login
    """
    # get parameter
    req_dict = request.get_json()
    mobile = req_dict.get("mobile")
    password = req_dict.get("password")
    # verify parameter
    if not all([mobile, password]):
        return jsonify(errno=RET.PRAMERR, errmsg="参数不完整")

    # phone number format
    if not re.match(r'1[34578]\d{9}', mobile):
        # wrong format
        return jsonify(errno=RET.PARAMERR, errmsg="手机号码格式错误")
    # error times
    user_ip = request.remote_addr
    try:
        access_nums = redis_store.get("access_nums_%s" % user_ip)
    except Exception as e:
        logging.error(e)
    else:
        if access_nums is not None and int(access_nums) >= constants.LOGIN_ERROR_MAX_TIMES:
            return jsonify(errno=RET.REQERR, errmsg="错误次数过多,请稍后重试")
    # fetch user by phone number
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='获取用户信息失败')

    # verify password
    # if login failed, record failed times
    logging.info(user.name)
    if user is None or not user.check_password(password):
        try:
            redis_store.incr("access_nums_%s" % user_ip)
            redis_store.expire("access_nums_%s" % user_ip, constants.LOGIN_ERROR_FORBID_TIME)
        except Exception as e:
            logging.error(e)
        
        return jsonify(errno=RET.DATAERR, errmsg='用户名或密码错误')
    # else, save status
    session['name'] = user.name
    session['mobile'] = user.mobile
    session['user_id'] = user.id

    return jsonify(errno=RET.OK, errmsg="登录成功")

@api.route('/session', methods=["GET"])
def check_login():
    name = session.get('name')
    if name is not None:
        return jsonify(errno=RET.OK, errmsg='true', data={'name':name})
    return jsonify(errno=RET.SESSIONERR, errmsg='false')

@api.route('/session', methods=['DELETE'])
def logout():
    session.clear()
    return jsonify(errno=RET.OK, errmsg="OK")
