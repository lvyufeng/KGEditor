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
@api.route('/project', methods=['POST'])
@login_required
def add_project():
    """新建项目
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


@api.route('/add_graph_to_project', methods=['POST'])
@login_required
def add_graph_to_project():
    """添加图谱到项目
    param:  project_id
            graph_id
    """
    # pass
    req_dict = request.get_json()
    project_id = req_dict['project_id']
    graph_id = req_dict['graph_id']
    try:
        project = Project.query.filter_by(id=project_id).first()
        graph = Graph.query.filter_by(id=graph_id).first()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    else:
        if not all([project, graph]):
            return jsonify(errno=RET.USERERR, errmsg='用户无权操作项目或图谱')
    if graph.project_id is not None:
            return jsonify(errno=RET.DATAEXIST, errmsg='图谱已绑定项目')
    try:
        graph.project_id = project.id
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    return jsonify(errno=RET.OK, errmsg="绑定成功")

@api.route('/add_partner', methods=['POST'])
@login_required
def add_partner():
    """添加协作者(Todo)
    
    """
    # pass
    return jsonify(errno=RET.OK, errmsg="添加成功")

# update


# retrieval
@api.route('/list_projects', methods=['GET'])
@login_required
def list_projects():
    """项目列表
    
    """
    project_list = []
    user_id = g.user_id
    try:
        projects = Project.query.filter_by(creator_id=user_id).all()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')

    for project in projects:
        project_list.append(project.to_dict())
    return jsonify(errno=RET.OK, errmsg="查询成功", data=project_list)

@api.route('/list_unlinked_graphs', methods=['POST'])
@login_required
def list_unlinked_graphs():
    """Todo
    """
    # pass
    return jsonify(errno=RET.OK, errmsg="删除成功")

# delete
@api.route('/delete_project', methods=['GET'])
@login_required
def delete_project():
    """删除项目
    
    """
    # pass
    return jsonify(errno=RET.OK, errmsg="删除成功")

@api.route('/remove_partner', methods=['POST'])
@login_required
def remove_partner():
    """删除协作者
    
    """
    # pass
    return jsonify(errno=RET.OK, errmsg="添加成功")

@api.route('/remove_graph', methods=['POST'])
@login_required
def remove_graph():
    """移除图谱
    
    """
    # pass
    return jsonify(errno=RET.OK, errmsg="添加成功")
