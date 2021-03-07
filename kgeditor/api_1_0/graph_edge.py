from . import api
from flask import jsonify, g, request, session
from kgeditor.utils.common import login_required, verify_domain, verify_graph
from kgeditor.utils.data import text2json
from kgeditor import db, arango_conn
from kgeditor.models import Graph
from kgeditor.utils.response_code import RET
from sqlalchemy.exc import IntegrityError
import logging
from pyArango.theExceptions import *
import json

# list edge collections
@api.route('/<int:domain_id>/graph/<int:graph_id>/edge', methods=['GET'])
@login_required
@verify_graph
def list_edge_collections(domain_id, graph_id):
    """展示关系类型
    
    Args:
        graph_id: graph to show the vertex collections
    """
    domain_db = arango_conn['domain_{}'.format(domain_id)]
    db_graph = domain_db.graphs['graph_{}'.format(graph_id)]

    url = f'{db_graph.getURL()}/edge'
    resp = arango_conn.session.get(url)
    if resp.status_code != 200:
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    data = text2json(resp.text)
    return jsonify(errno=RET.OK, errmsg="OK", data=data['collections'])

# add edge
@api.route('/<int:domain_id>/graph/<int:graph_id>/edge/<collection>', methods=['POST'])
@login_required
@verify_graph
def add_edge(domain_id, graph_id, collection):
    """add edge
    """
    domain_db = arango_conn['domain_{}'.format(domain_id)]
    db_graph = domain_db.graphs['graph_{}'.format(graph_id)]
    req = request.get_json()
    _from = req['from']
    _to = req['to']
    attribute = req['attribute']
    if not all([_from, _to]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    try:
        db_graph.createEdge(collection, _from, _to, attribute)
    except CreationError as e:
        logging.error(e)
        return jsonify(errno=RET.DATAEXIST, errmsg="添加边失败")
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg="添加边失败")
    return jsonify(errno=RET.OK, errmsg="添加边成功")
# get edge
@api.route('/<int:domain_id>/graph/<int:graph_id>/edge/<collection>/<edge>', methods=['GET'])
@login_required
def get_edge(domain_id, graph_id, collection, edge):
    domain_db = arango_conn['domain_{}'.format(domain_id)]
    db_graph = domain_db.graphs['graph_{}'.format(graph_id)]
    url = "%s/edge/%s/%s" % (db_graph.getURL(), collection, edge)
    try:
        r = db_graph.connection.session.get(url)        
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询失败")
    if r.status_code == 200:
        data = r.json()
        return jsonify(errno=RET.OK, errmsg="查询成功", data=data['edge'])
    return jsonify(errno=RET.DBERR, errmsg="查询失败")

# delete edge
@api.route('/<int:domain_id>/graph/<int:graph_id>/edge/<collection>/<edge>', methods=['DELETE'])
@login_required
def delete_edge(domain_id, graph_id, collection, edge):
    # pass
    domain_db = arango_conn['domain_{}'.format(domain_id)]
    db_graph = domain_db.graphs['graph_{}'.format(graph_id)]
    
    try:
        document = domain_db[collection][edge]
        db_graph.deleteEdge(document)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg="删除失败")
    return jsonify(errno=RET.OK, errmsg="删除成功")

# update edge
@api.route('/<int:domain_id>/graph/<int:graph_id>/edge/<collection>/<edge>', methods=['PATCH'])
@login_required
def update_edge(domain_id, graph_id, collection, edge):
    # pass
    domain_db = arango_conn['domain_{}'.format(domain_id)]
    db_graph = domain_db.graphs['graph_{}'.format(graph_id)]
    url = "%s/vertex/%s/%s" % (db_graph.getURL(), collection, edge)
    req = request.get_json()
    if not req:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    try:
        r = db_graph.connection.session.patch(url, data = json.dumps(req, default=str))        
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg="修改失败")
    if r.status_code == 200 or r.status_code == 202:
        return jsonify(errno=RET.OK, errmsg="修改成功")
    return jsonify(errno=RET.DBERR, errmsg="修改失败")