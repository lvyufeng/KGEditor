from . import api
from flask import jsonify
from kgeditor.utils.response_code import RET
from kgeditor.utils.common import login_required

# CRUD
# create
@api.route('/add_project', methods=['GET'])
@login_required
def add_project():
    # pass
    return jsonify(errno=RET.OK, errmsg="添加成功")

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
