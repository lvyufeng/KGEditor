"""
entity and relation types are defined as collection in ArangoDB,
and all operations of them are assigned in this file
"""
from . import api
from flask import jsonify, g, request, session
from kgeditor.utils.common import login_required
from kgeditor import db, arango_conn
from kgeditor.models import Graph
from kgeditor.utils.response_code import RET
from sqlalchemy.exc import IntegrityError
import logging
from pyArango.consts import *

@api.route('list_documents', methods=['POST'])
@login_required
def list_documents():
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
    
    documents = []
    graph_db = arango_conn['graph_{}'.format(graph_id)]
    
    for name, collection in graph_db.collections.items():
        if collection.type == COLLECTION_DOCUMENT_TYPE and not name.startswith('_'):
            documents.append(name)
    return jsonify(errno=RET.OK, errmsg="OK", data=documents)

@api.route('list_edges', methods=['POST'])
@login_required
def list_edges():
    req_dict = request.get_json()
    graph_id = req_dict.get('graph_id')
    try:
        graph = Graph.query.filter_by(id=graph_id, creator_id=g.user_id).first()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    else:
        if graph is None:
            return jsonify(errno=RET.DBERR, errmsg='边集合不存在或用户无编辑权限')
    graph_db = arango_conn['graph_{}'.format(graph_id)]
    # graph_db.collections
    edges = []
    for name, collection in graph_db.collections.items():
        if collection.type == COLLECTION_EDGE_TYPE:
            edges.append(name)
    # logging.info(graph_db.collections)
    return jsonify(errno=RET.OK, errmsg="OK", data=edges)

