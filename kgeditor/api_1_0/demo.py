from . import api
from flask import current_app
import logging
from kgeditor import db, models
from kgeditor.utils.common import login_required

@api.route("/demo")
def index():
    logging.debug('info msg')
    logging.info('info msg')
    logging.warn('info msg')
    return "index"

@api.route('/get_public_graphs', methods=['GET'])
@login_required
def get_public_graphs():
    # pass
    return jsonify(errno=RET.OK, errmsg="删除成功")

