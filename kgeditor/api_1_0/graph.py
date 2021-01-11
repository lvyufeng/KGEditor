from . import api
from kgeditor.utils.common import login_required
# CRUD
# create
@api.route('/create_graph', methods=['POST'])
@login_required
def create_graph():
    # pass
    return jsonify(errno=RET.OK, errmsg="删除成功")

@api.route('/add_node', methods=['POST'])
@login_required
def add_node():
    # pass
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
    return jsonify(errno=RET.OK, errmsg="删除成功")

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
    return jsonify(errno=RET.OK, errmsg="删除成功")

@api.route('/delete_node', methods=['POST'])
@login_required
def delete_node():
    # pass
    return jsonify(errno=RET.OK, errmsg="删除成功")

