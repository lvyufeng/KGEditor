from . import api
from flask import jsonify, g, request, session
from kgeditor.utils.common import login_required, verify_domain, verify_graph
from kgeditor import db, arango_conn
from kgeditor.models import Graph
from kgeditor.utils.response_code import RET
from sqlalchemy.exc import IntegrityError
import logging
from pyArango.theExceptions import *
import json
# CURD
# create graph
@api.route('<domain_id>/graph', methods=['POST'])
@login_required
def create_graph(domain_id):
    """新建图谱
    create graph
    Args:
        name:
        private:
    Returns
    """
    # get request json, return dict
    user_id = g.user_id
    req_dict = request.get_json()
    name = req_dict.get('name')
    private = req_dict.get('private')
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

# retrieve one domain
@api.route('/<int:domain_id>/graph', methods=['GET'])
@login_required
def list_graphs(domain_id):
    """所有图谱
    """
    graph_list = []
    user_id = g.user_id
    try:
        graphs = Graph.query.filter_by(creator_id=user_id, domain_id=domain_id).all()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    logging.info(graphs)
    for graph in graphs:
        graph_list.append(graph.to_dict())
    return jsonify(errno=RET.OK, errmsg="查询成功", data=graph_list)

# retrieve all
@api.route('/all/graph', methods=['GET'])
@login_required
def list_all_graphs():
    """所有图谱
    """
    graph_list = []
    user_id = g.user_id
    try:
        graphs = Graph.query.filter_by(creator_id=user_id).all()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    logging.info(graphs)
    for graph in graphs:
        graph_list.append(graph.to_dict())
    return jsonify(errno=RET.OK, errmsg="查询成功", data=graph_list)

# delete
@api.route('/<int:domain_id>/graph/<int:graph_id>', methods=['DELETE'])
@login_required
@verify_graph
def delete_graph(domain_id, graph_id):
    """删除图谱
    """
    # pass
    graph = g.graph
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

# show graph info
@api.route('/<int:domain_id>/graph/<int:graph_id>', methods=['GET'])
@login_required
@verify_graph
def show_graph(domain_id, graph_id):
    domain_db = arango_conn['domain_{}'.format(domain_id)]
    graph = domain_db.graphs['graph_{}'.format(graph_id)]
    collections = []
    edges = []
    for k, v in graph.definitions.items():
        edges.append(k)
        collections.extend(v.fromCollections)
        collections.extend(v.toCollections)
    collections = list(set(collections))
    collections.extend(graph._orphanedCollections)
    return jsonify(errno=RET.OK, errmsg="OK", data={'collections': collections, 'edges':edges})


@api.route('/<int:domain_id>/graph/<int:graph_id>/traverse', methods=['POST'])
@login_required
@verify_graph
def traversal(domain_id, graph_id):
    """图遍历
    
    Args:
        startVertex: the start vertex to show, eg. "persons/alice"
        direction: direction for traversal
            if set, must be either "outbound", "inbound", or "any"
            if not set, the expander attribute must be specified
        maxDepth: visits only nodes in at most the given depth
        minDepth: visits only nodes in at least the given depth
    """
    domain_db = arango_conn['domain_{}'.format(domain_id)]
    db_graph = domain_db.graphs['graph_{}'.format(graph_id)]
    req_dict = request.get_json()
    startVertex = req_dict.pop('startVertex')

    req_dict["uniqueness"] =  {"vertices": "global", "edges": "global"}
    data = db_graph.traverse(startVertex, **req_dict)

    return jsonify(errno=RET.OK, errmsg="OK", data=data['visited'])





