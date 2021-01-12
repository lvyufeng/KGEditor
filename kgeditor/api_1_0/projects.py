import logging
from . import api
from flask import jsonify, g, request
from kgeditor.utils.response_code import RET
from kgeditor.utils.common import login_required
from kgeditor.models import Project, Graph
from sqlalchemy.exc import IntegrityError
from kgeditor import db, redis_store, constants

# CRUD
# create
@api.route('/add_project', methods=['POST'])
@login_required
def add_project():
    """
    add project
    """
    user_id = g.user_id
    req_dict = request.get_json()
    name = req_dict.get('name')
    graph_id = req_dict.get('graph_id')
    if not name:
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")
    try:
        project = Project.query.filter_by(name=name).first()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    else:
        if project is not None:
            return jsonify(errno=RET.DATAEXIST, errmsg='项目已存在')
    # 5.save graph info to db
    project = Project(name=name, creator_id=user_id)
    try:
        db.session.add(project)
        # bind graph
        if graph_id:
            try:
                graph = Graph.query.filter_by(id=graph_id, creator_id=user_id, project_id=None).first()
            except Exception as e:
                db.session.rollback()
                logging.error(e)
                return jsonify(errno=RET.DBERR, errmsg='数据库异常')
            else:
                if graph is None:
                    return jsonify(errno=RET.USERERR, errmsg='登录用户没有操作图谱权限或图谱已绑定项目')
                graph.project_id = project.id
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        # phone number duplicate
        logging.error(e)
        return jsonify(errno=RET.DATAEXIST, errmsg='项目已存在')
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据库异常')
    # add graph to project if graph_id is not None
    
    return jsonify(errno=RET.OK, errmsg="新建项目成功")


@api.route('/add_graph', methods=['POST'])
@login_required
def add_graph():
    # pass
    return jsonify(errno=RET.OK, errmsg="添加成功")

@api.route('/add_partner', methods=['POST'])
@login_required
def add_partner():
    # pass
    return jsonify(errno=RET.OK, errmsg="添加成功")

# update


# retrieval
@api.route('/list_projects', methods=['POST'])
@login_required
def list_projects():
    # pass
    return jsonify(errno=RET.OK, errmsg="删除成功")

@api.route('/list_unlinked_graphs', methods=['POST'])
@login_required
def list_unlinked_graphs():
    # pass
    return jsonify(errno=RET.OK, errmsg="删除成功")

# delete
@api.route('/delete_project', methods=['GET'])
@login_required
def delete_project():
    # pass
    return jsonify(errno=RET.OK, errmsg="删除成功")

@api.route('/remove_partner', methods=['POST'])
@login_required
def remove_partner():
    # pass
    return jsonify(errno=RET.OK, errmsg="添加成功")

@api.route('/remove_graph', methods=['POST'])
@login_required
def remove_graph():
    # pass
    return jsonify(errno=RET.OK, errmsg="添加成功")
