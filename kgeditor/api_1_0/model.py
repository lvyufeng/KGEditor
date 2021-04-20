import logging
from . import api
from flask import jsonify, g, request, session
from kgeditor.utils.common import login_required
from kgeditor import db, arango_conn
from kgeditor.models import Model
from kgeditor.utils.response_code import RET
from sqlalchemy.exc import IntegrityError
from pyArango.theExceptions import CreationError

@api.route('/model', methods=['POST'])
@login_required
def add_model():
    """Add Model

    Add model to serve all projects

    Args:
        name: 

    Returns:
        pass
    """
    # get request json, return dict
    user_id = g.user_id
    req_dict = request.get_json()
    name = req_dict.get('name')
    model_type = req_dict.get('type')
    url = req_dict.get('url')
    private = req_dict.get('private')
    discription = req_dict.get('discription')

    if None in [name, url, model_type, private]:
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")
    try:
        domain = Model.query.filter_by(name=name).first()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    else:
        if domain is not None:
            return jsonify(errno=RET.DATAEXIST, errmsg='"{}"模型已存在'.format(name))

    model = Model(name=name, creator_id=user_id, model_type=model_type, url=url, private=private, discription=discription)
    try:
        db.session.add(model)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='添加模型失败')
    
    return jsonify(errno=RET.OK, errmsg="添加模型成功")

@api.route('/model', methods=['GET'])
@login_required
def list_model():
    """Query all models
    
    """
    try:
        model_list = Model.query.all()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    model_dict_list = []
    for model in model_list:
        model_dict_list.append(model.to_dict())
    
    return jsonify(errno=RET.OK, errmsg="OK", data=model_dict_list)

@api.route('/model/<model_id>', methods=['DELETE'])
@login_required
def delete_model(model_id):
    """Delete model by id
    
    """
    user_id = g.user_id
    req_dict = request.get_json()
    if not model_id:
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")
    try:
        model = Model.query.filter_by(id=model_id, creator_id=user_id).first()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    else:
        if model is None:
            return jsonify(errno=RET.DATAEXIST, errmsg='模型不存在')
    # 5.save graph info to db
    try:
        db.session.delete(model)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='删除模型失败')     
    return jsonify(errno=RET.OK, errmsg="删除模型成功")

@api.route('/model/<model_id>', methods=['PATCH'])
@login_required
def modify_model(model_id):
    """Modify model informations
    
    """
    user_id = g.user_id
    req_dict = request.get_json()
    name = req_dict.get('name')
    model_type = req_dict.get('type')
    url = req_dict.get('url')
    private = req_dict.get('private')
    discription = req_dict.get('discription')

    if None in [model_id, model_type, url, private, discription]:
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
    try:
        model = Model.query.filter_by(id=model_id).first()
        model.name = name
        model.model_type = model_type
        model.url = url
        model.private = private
        model.discription = discription
        db.session.commit()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    return jsonify(errno=RET.OK, errmsg="修改成功")


@api.route('/<model_type>/model', methods=['GET'])
@login_required
def list_type_model(model_type):
    """Query all models
    
    """
    try:
        model_list = Model.query.filter_by(model_type=model_type).all()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    model_dict_list = []
    for model in model_list:
        model_dict_list.append(model.to_dict())
    
    return jsonify(errno=RET.OK, errmsg="OK", data=model_dict_list)