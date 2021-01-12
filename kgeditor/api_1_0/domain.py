import logging
from . import api
from flask import jsonify, g, request, session
from kgeditor.utils.common import login_required
from kgeditor import db
from kgeditor.models import Domain
from kgeditor.utils.response_code import RET
from sqlalchemy.exc import IntegrityError

@api.route('/add_domain', methods=['POST'])
@login_required
def add_domain():
    # pass
    # get request json, return dict
    user_id = g.user_id
    req_dict = request.get_json()
    name = req_dict.get('name')
    if not name:
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")
    try:
        domain = Domain.query.filter_by(name=name).first()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    else:
        if domain is not None:
            return jsonify(errno=RET.DATAEXIST, errmsg='{name}领域已存在')
    # 5.save graph info to db
    domain = Domain(name=name, creator_id=user_id)
    try:
        db.session.add(domain)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        # phone number duplicate
        logging.error(e)
        return jsonify(errno=RET.DATAEXIST, errmsg='领域已存在')
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据库异常')
    # 6. use neo4j create graph

    # 6.save login status to session
    # session['domain_id'] = domain.id
    
    return jsonify(errno=RET.OK, errmsg="新建图谱成功")


@api.route('/list_domain', methods=['GET'])
@login_required
def list_domain():
    # pass
    # get request json, return dict
    try:
        domain_list = Domain.query.all()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    domain_dict_list = []
    for domain in domain_list:
        domain_dict_list.append(domain.to_dict())
    
    return jsonify(errno=RET.OK, errmsg="OK", data=domain_dict_list)

@api.route('/rename_domain', methods=['POST'])
@login_required
def rename_domain():
    # pass
    # get request json, return dict
    req_dict = request.get_json()
    domain_id = req_dict.get('domain_id')
    name = req_dict.get('name')
    if not all([domain_id, name]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数错误')
    try:
        domain = Domain.query.filter_by(id=domain_id).first()
        domain.name = name
        db.session.commit()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    return jsonify(errno=RET.OK, errmsg="修改成功")