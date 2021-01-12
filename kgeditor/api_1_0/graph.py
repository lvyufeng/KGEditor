from . import api
from flask import jsonify, g, request, session
from kgeditor.utils.common import login_required
from kgeditor import db, arango_conn
from kgeditor.models import Graph
from kgeditor.utils.response_code import RET
from sqlalchemy.exc import IntegrityError
import logging
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
    logging.info([name, private, domain_id])
    if None in [name, private, domain_id]:
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")
    try:
        graph = Graph.query.filter_by(name=name).first()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    else:
        if graph is not None:
            return jsonify(errno=RET.DATAEXIST, errmsg='"{}"图谱已存在'.format(name))
    # 5.save graph info to db
    graph = Graph(name=name, private=private, creator_id=user_id, domain_id=domain_id)
    try:
        db.session.add(graph)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        # phone number duplicate
        logging.error(e)
        return jsonify(errno=RET.DATAEXIST, errmsg='图谱已存在')
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据库异常')
    # 6. use arango create graph
    try:
        arango_conn.createDatabase(name="graph_{}".format(graph.id))
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='添加图数据库失败')
    # system_graph = neo4j
    # system_graph.run('CREATE DATABASE subgraph_{}'.format(graph.id))
    # logging.info(subgraph)
    # 6.save login status to session
    # session['graph_id'] = graph.id
    
    return jsonify(errno=RET.OK, errmsg="新建图谱成功")

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
@api.route('/list_graphs', methods=['GET'])
@login_required
def list_graphs():
    # pass
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

