import os
import json
import logging
import pymysql
from . import api
from flask import jsonify, request, g
from kgeditor import db, models, data, file_path, text
from kgeditor.utils.common import login_required
from kgeditor.utils.response_code import RET
from kgeditor.models import Data
from flask_uploads import UploadSet, DATA, configure_uploads, ALL
from kgeditor.constants import DATA_MONGO, DATA_MYSQL, DATA_TEXT
# import json and csv
dtype_dict = {
    'text': text,
    'data': data
}

def upload_raw_file(dtype, is_raw=True):
    user_id = g.user_id
    request_form = request.form.to_dict()
    name = request_form.get('name')
    data_type = int(request_form.get('data_type'))
    private = bool(request_form.get('private'))
    if None in [name, data_type, private]:
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")
    if data_type != DATA_TEXT:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    
    if 'data' not in request.files:
        return jsonify(errno=RET.PARAMERR, errmsg="未获取到上传文件")
    try:
        file_name = dtype_dict.get(dtype).save(request.files['data'])
        logging.info(file_name)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.IOERR, errmsg="文件上传失败")
    d = Data(name=name, data_type=DATA_TEXT, creator_id=user_id, private=True, data_info=os.path.join(file_path, file_name), is_raw=is_raw)
    try:
        db.session.add(d)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='添加数据失败')
    
    return jsonify(errno=RET.OK, errmsg="添加数据成功")

def add_db():
    user_id = g.user_id
    req_dict = request.get_json()
    data_type = req_dict.pop('data_type')
    private = req_dict.pop('private')
    name = req_dict.pop('name')
    if None in [name, data_type, private]:
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")
    if data_type not in (DATA_MONGO, DATA_MYSQL):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    if data_type == DATA_MYSQL:
        try:
            test_db = pymysql.connect(
                host = req_dict['ip'],
                port = int(req_dict['port']),
                user = req_dict['username'],
                password = req_dict['password'],
                database = req_dict['db']
            )
        except Exception as e:
            logging.error(e)
            return jsonify(errno=RET.DBERR, errmsg='数据库连接测试失败')
        else:
            test_db.close()
    
    data = Data(name=name, data_type=data_type, creator_id=user_id, private=private, data_info=json.dumps(req_dict), is_raw=True)
    try:
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='添加数据失败')
    
    return jsonify(errno=RET.OK, errmsg="添加数据成功")


@api.route('/raw_data', methods=['POST'])
@login_required
def add_raw_data():
    """Add raw data
    """
    # get request json, return dict
    request_files = request.files.to_dict()
    if request_files:
        return upload_raw_file('text')
    else:
        return add_db()

@api.route('/raw_data', methods=['GET'])
@login_required
def fetch_raw_data():
    """Fetch raw data
    """
    user_id = g.user_id
    try:
        data_list = Data.query.filter_by(creator_id=user_id, is_raw=True).all()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    data_dict_list = []
    for data in data_list:
        data_dict_list.append(data.to_dict())
    
    return jsonify(errno=RET.OK, errmsg="OK", data=data_dict_list)

@api.route('/triple_data', methods=['POST'])
@login_required
def add_triple_data():
    """Add triple data
    """
    return upload_raw_file('data', False)


@api.route('/triple_data', methods=['GET'])
@login_required
def fetch_triple_data():
    """Fetch raw data
    """
    user_id = g.user_id
    try:
        data_list = Data.query.filter_by(creator_id=user_id, is_raw=False).all()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    data_dict_list = []
    for data in data_list:
        data_dict_list.append(data.to_dict())
    
    return jsonify(errno=RET.OK, errmsg="OK", data=data_dict_list)