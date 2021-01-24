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
    """
    create graph
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
    """
    add node
    """
    # verify graph_id
    # session
    return jsonify(errno=RET.OK, errmsg="删除成功")

@api.route('/add_in_relation', methods=['POST'])
@login_required
def add_in_relation():
    # pass
    return jsonify(errno=RET.OK, errmsg="删除成功")

@api.route('/add_out_relation', methods=['POST'])
@login_required
def add_out_relation():
    # pass
    return jsonify(errno=RET.OK, errmsg="删除成功")

# update
@api.route('/change_domain', methods=['POST'])
@login_required
def change_domain():
    # pass
    return jsonify(errno=RET.OK, errmsg="删除成功")

@api.route('/change_nodel_relation', methods=['POST'])
@login_required
def change_nodel_relation():
    # pass
    return jsonify(errno=RET.OK, errmsg="删除成功")


# retrieval
@api.route('/list_graphs', methods=['POST'])
@login_required
def list_graphs():
    # pass
    graph_list = []
    user_id = g.user_id
    req_dict = request.get_json()
    domain_id = req_dict.get('domain_id')   
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


@api.route('/get_node', methods=['POST'])
@login_required
def get_node():
    # pass
    return jsonify(errno=RET.OK, errmsg="删除成功")

@api.route('/get_neighbor', methods=['POST'])
@login_required
def get_neighbor():
    # pass
    return jsonify(errno=RET.OK, errmsg="删除成功")

@api.route('/show_vertex', methods=['GET'])
@login_required
def show_graph():
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
    graph = domain_db.graphs['graph_{}'.format(graph_id)]
    logging.info(graph.getURL())
    url = f'{graph.getURL()}/vertex'
    resp = arango_conn.session.get(url)
    if resp.status_code != 200:
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    data = text2json(resp.text)

    # collections = []
    # edges = []
    # for k, v in graph.definitions.items():
    #     edges.append(k)
    #     collections.extend(v.fromCollections)
    #     collections.extend(v.toCollections)
    # collections = list(set(collections))
    # collections.extend(graph._orphanedCollections)
    return jsonify(errno=RET.OK, errmsg="OK", data=data['collections'])
# delete
@api.route('/delete_graph', methods=['POST'])
@login_required
def delete_graph():
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

