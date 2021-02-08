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

# list vertex collections
@api.route('/<int:domain_id>/graph/<int:graph_id>/vertex', methods=['GET'])
@login_required
@verify_graph
def list_vertex_collections(domain_id, graph_id):
    """展示实体类型
    
    Args:
        graph_id: graph to show the vertex collections
    """
    domain_db = arango_conn['domain_{}'.format(domain_id)]
    db_graph = domain_db.graphs['graph_{}'.format(graph_id)]

    url = f'{db_graph.getURL()}/vertex'
    resp = arango_conn.session.get(url)
    if resp.status_code != 200:
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    data = text2json(resp.text)
    return jsonify(errno=RET.OK, errmsg="OK", data=data['collections'])

# list one vertex collection
@api.route('/<int:domain_id>/graph/<int:graph_id>/vertex/<string:collection>', methods=['GET'])
@login_required
@verify_graph
def list_one_collection(domain_id, graph_id, collection):
    """展示实体列表
    Args:
        page: page number 
        len: page length (vertex number in one page)
    """
    page = request.args.get('page')
    page_len = request.args.get('len')
    try:
        page = int(page)
        page_len = int(page_len)
        domain_db = arango_conn['domain_{}'.format(domain_id)]
        collection = domain_db.collections[collection]
    except KeyError as e:
        logging.info(e)
        return jsonify(errno=RET.DATAERR, errmsg="不存在该集合")
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    if page < 1:
        return jsonify(errno=RET.PARAMERR, errmsg="页数小于1")
    count = collection.count()
    if page_len * (page - 1) > count:
        return jsonify(errno=RET.PARAMERR, errmsg="请求错误")
    data = collection.fetchAll(limit = page_len, skip = page_len * (page - 1))
    pages = int(count / page_len) + 1

    return jsonify(errno=RET.OK, errmsg="OK", data={'vertex': data.result, 'pages': pages, 'count':count})

@api.route('/<int:domain_id>/graph/<int:graph_id>/vertex/<collection>', methods=['POST'])
@login_required
@verify_graph
def add_node(domain_id, graph_id, collection):
    """添加节点
    add node
    """
    # verify graph_id
    # session
    domain_db = arango_conn['domain_{}'.format(domain_id)]
    db_graph = domain_db.graphs['graph_{}'.format(graph_id)]
    req = request.get_json()
    name = req['name']
    if not name:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    attribute = req['attribute']
    if attribute is not None:
        attribute['name'] = name
    else:
        attribute = {'name': name}
    try:
        db_graph.createVertex(collection, attribute)
    except CreationError as e:
        logging.error(e)
        return jsonify(errno=RET.DATAEXIST, errmsg="添加节点失败")
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg="添加节点失败")
    return jsonify(errno=RET.OK, errmsg="添加节点成功")

@api.route('/<int:domain_id>/graph/<int:graph_id>/vertex/<collection>/<vertex>', methods=['DELETE'])
@login_required
def delete_node(domain_id, graph_id, collection, vertex):
    # pass
    domain_db = arango_conn['domain_{}'.format(domain_id)]
    db_graph = domain_db.graphs['graph_{}'.format(graph_id)]
    
    try:
        document = domain_db[collection][vertex]
        db_graph.deleteVertex(document)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.OK, errmsg="删除失败")
    return jsonify(errno=RET.OK, errmsg="删除成功")