import logging
from flask import jsonify
from kgeditor import db, models
from kgeditor.utils.common import login_required
from kgeditor.utils.response_code import RET
from kgeditor.models import Graph
from . import api

@api.route("/demo")
def index():
    logging.debug('info msg')
    logging.info('info msg')
    logging.warn('info msg')
    return "index"

@api.route('/public_graph', methods=['GET'])
def get_public_graphs():
    graph_list = []
    try:
        graphs = Graph.query.filter_by(private=False).all()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    for graph in graphs:
        graph_list.append(graph.to_dict())
    return jsonify(errno=RET.OK, errmsg="查询成功", data=graph_list)
