from flask import session, jsonify, g, request, abort
from kgeditor.utils.response_code import RET
import functools
from kgeditor.models import Domain, Graph
import logging
# verify login status
def login_required(view_func):
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        user_id = session.get('user_id')
        if user_id is not None:
            g.user_id = user_id
            return view_func(*args, **kwargs)
        else:
            return abort(401, 'User unauthorized.')
            # return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")
    return wrapper

# verify domain
def verify_domain(view_func):
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        req_dict = request.get_json()
        domain_id = req_dict.get('domain_id')
        # validate permission
        try:
            domain = Domain.query.filter_by(id=domain_id, creator_id=g.user_id).first()
        except Exception as e:
            logging.error(e)
            return jsonify(errno=RET.DBERR, errmsg='数据库异常')
        else:
            if domain is None:
                return jsonify(errno=RET.DBERR, errmsg='领域不存在或用户无编辑权限')
            g.domain_id = domain_id
            return view_func(*args, **kwargs)
    return wrapper            

# verify graph
def verify_graph(view_func):
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        # validate permission
        logging.info(kwargs)
        try:
            graph = Graph.query.filter_by(id=kwargs['graph_id'], domain_id=kwargs['domain_id'], creator_id=g.user_id).first()
        except Exception as e:
            logging.error(e)
            return jsonify(errno=RET.DBERR, errmsg='数据库异常')
        else:
            if graph is None:
                return jsonify(errno=RET.DBERR, errmsg='图谱不存在或用户无编辑权限')
            g.graph = graph
            return view_func(*args, **kwargs)
    return wrapper