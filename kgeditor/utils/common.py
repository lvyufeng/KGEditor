from flask import session, jsonify, g, request
from kgeditor.utils.response_code import RET
import functools
from kgeditor.models import Graph
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
            return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")
    return wrapper

# verify graph
def verify_graph(view_func):
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        req_dict = request.get_json()
        graph_id = req_dict.get('graph_id')
        # validate permission
        try:
            graph = Graph.query.filter_by(id=graph_id, creator_id=g.user_id).first()
        except Exception as e:
            logging.error(e)
            return jsonify(errno=RET.DBERR, errmsg='数据库异常')
        else:
            if graph is None:
                return jsonify(errno=RET.DBERR, errmsg='文档集合不存在或用户无编辑权限')
            g.graph_id = graph_id
            return view_func(*args, **kwargs)
    return wrapper            