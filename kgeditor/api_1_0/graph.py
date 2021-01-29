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
# CRUD
# create
@api.route('/create_graph', methods=['POST'])
@login_required
def create_graph():
    """新建图谱
    create graph
    Args:
        name:
        domain_id:
        private:
    Returns
    """
    # get request json, return dict
    user_id = g.user_id
    req_dict = request.get_json()
    name = req_dict.get('name')
    private = req_dict.get('private')
    domain_id = req_dict.get('domain_id')
    # logging.info([name, private, domain_id])
    # if None in [name, private, domain_id]:
    #     return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")
    # try:
    #     graph = Graph.query.filter_by(name=name).first()
    # except Exception as e:
    #     logging.error(e)
    #     return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    # else:
    #     if graph is not None:
    #         return jsonify(errno=RET.DATAEXIST, errmsg='"{}"图谱已存在'.format(name))
    # # 5.save graph info to db
    # graph = Graph(name=name, private=private, creator_id=user_id, domain_id=domain_id)
    # try:
    #     db.session.add(graph)
    #     db.session.commit()
    #     arango_db = arango_conn["domain_{}".format(domain_id)]
    #     arango_db.createGraph("graph_{}".format(graph.id))
    # except IntegrityError as e:
    #     db.session.rollback()
    #     # phone number duplicate
    #     logging.error(e)
    #     return jsonify(errno=RET.DATAEXIST, errmsg='图谱已存在')
    # except CreationError as e:
    #     logging.error(e)
    #     return jsonify(errno=RET.DBERR, errmsg='创建图谱失败')
    # except Exception as e:
    #     db.session.rollback()
    #     logging.error(e)
    #     return jsonify(errno=RET.DBERR, errmsg='查询数据库异常')
    
    return jsonify(errno=RET.OK, errmsg="新建图谱成功")

# add entity type

# add relation type

# list entity type

# list relation type

@api.route('/add_node', methods=['POST'])
@login_required
def add_node():
    """添加节点
    add node
    """
    # verify graph_id
    # session
    return jsonify(errno=RET.OK, errmsg="删除成功")

@api.route('/add_in_relation', methods=['POST'])
@login_required
def add_in_relation():
    """添加In关系
    """
    # pass
    return jsonify(errno=RET.OK, errmsg="删除成功")

@api.route('/add_out_relation', methods=['POST'])
@login_required
def add_out_relation():
    """添加Out关系
    
    """
    
    # pass
    return jsonify(errno=RET.OK, errmsg="删除成功")

# retrieval
@api.route('/list_graphs', methods=['GET'])
@login_required
def list_graphs():
    """所有图谱
    """
    # pass
    graph_list = []
    user_id = g.user_id
    domain_id = request.args.get('domain_id')
    try:
        if domain_id == None:
            graphs = Graph.query.filter_by(creator_id=user_id).all()
        else:
            graphs = Graph.query.filter_by(creator_id=user_id, domain_id=domain_id).all()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    logging.info(graphs)
    for graph in graphs:
        graph_list.append(graph.to_dict())
    return jsonify(errno=RET.OK, errmsg="查询成功", data=graph_list)

@api.route('/show_vertex', methods=['GET'])
@login_required
def show_vertex():
    """展示实体类型
    
    Args:
        graph_id: graph to show the vertex collections
    """
    graph_id = request.args.get('graph_id')
    try:
        graph = Graph.query.filter_by(id=graph_id, creator_id=g.user_id).first()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    else:
        if graph is None:
            return jsonify(errno=RET.DBERR, errmsg='图谱不存在或用户无编辑权限')

    domain_db = arango_conn['domain_{}'.format(graph.domain_id)]
    db_graph = domain_db.graphs['graph_{}'.format(graph_id)]
    logging.info(db_graph.getURL())
    url = f'{db_graph.getURL()}/vertex'
    resp = arango_conn.session.get(url)
    if resp.status_code != 200:
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    data = text2json(resp.text)
    session['domain_id'] = graph.domain_id
    session['graph_id'] = graph_id
    return jsonify(errno=RET.OK, errmsg="OK", data=data['collections'])

@api.route('/vertex_list', methods=['GET'])
@login_required
def vertex_list():
    """展示实体列表
    Args:
        collection: name of vertex collection
        page: page number 
        len: page length (vertex number in one page)
    """
    collection_name = request.args.get('collection')
    page = request.args.get('page')
    page_len = request.args.get('len')
    domain_id = session.get('domain_id')
    try:
        page = int(page)
        page_len = int(page_len)
        domain_db = arango_conn['domain_{}'.format(domain_id)]
        collection = domain_db.collections[collection_name]
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
    # logging.info(type(data))
    return jsonify(errno=RET.OK, errmsg="OK", data={'vertex': data.result, 'pages': pages, 'count':count})

@api.route('/traverse', methods=['POST'])
@login_required
def traversal():
    """图遍历
    
    Args:
        startVertex: the start vertex to show, eg. "persons/alice"
        direction: direction for traversal
            if set, must be either "outbound", "inbound", or "any"
            if not set, the expander attribute must be specified
        maxDepth: visits only nodes in at most the given depth
        minDepth: visits only nodes in at least the given depth
    """
    graph_id = session.get('graph_id')
    domain_id = session.get('domain_id')
    if not all([graph_id, domain_id]):
        return jsonify(errno=RET.SESSIONERR, errmsg="未选择指定的图谱")
    logging.info(graph_id)
    logging.info(domain_id)
    domain_db = arango_conn['domain_{}'.format(domain_id)]
    db_graph = domain_db.graphs['graph_{}'.format(graph_id)]
    req_dict = request.get_json()
    startVertex = req_dict.pop('startVertex')
    direction = req_dict.get('direction')
    maxDepth = req_dict.get('maxDepth')
    minDepth = req_dict.get('minDepth')
    logging.info(req_dict)
    # logging.info()
    req_dict["uniqueness"] =  {"vertices": "global", "edges": "global"}

    data = db_graph.traverse(startVertex, **req_dict)

    return jsonify(errno=RET.OK, errmsg="OK", data=data['visited'])

@api.route('/show_graph', methods=['POST'])
@login_required
@verify_graph
def show_graph():
    domain_db = arango_conn['domain_{}'.format(g.domain_id)]
    graph = domain_db.graphs['graph_{}'.format(g.graph_id)]
    collections = []
    edges = []
    for k, v in graph.definitions.items():
        edges.append(k)
        collections.extend(v.fromCollections)
        collections.extend(v.toCollections)
    collections = list(set(collections))
    collections.extend(graph._orphanedCollections)
    return jsonify(errno=RET.OK, errmsg="OK", data={'collections': collections, 'edges':edges})
# delete
@api.route('/delete_graph', methods=['POST'])
@login_required
def delete_graph():
    """删除图谱
    """
    # pass
    user_id = g.user_id
    req_dict = request.get_json()
    graph_id = req_dict.get('graph_id')
    if not graph_id:
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")
    try:
        graph = Graph.query.filter_by(id=graph_id).first()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    else:
        if graph is None:
            return jsonify(errno=RET.DATAEXIST, errmsg='图谱不存在')
    # 5.save graph info to db
    try:
        db.session.delete(graph)
        db.session.commit()
        url = f'{arango_conn.getURL()}/database/graph_{graph_id}'
        arango_conn.session.delete(url)
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='删除图谱失败')    
    return jsonify(errno=RET.OK, errmsg="删除图谱成功")

@api.route('/delete_node', methods=['POST'])
@login_required
def delete_node():
    # pass
    return jsonify(errno=RET.OK, errmsg="删除成功")

