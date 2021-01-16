from . import api
from flask import jsonify
import logging
from kgeditor import db, models
from kgeditor.utils.common import login_required
from kgeditor.utils.response_code import RET
from kgeditor.models import Graph
from flask_uploads import UploadSet, DATA, configure_uploads, ALL
# import json amd csv
@api.route('/import_data')
@login_required
def import_data():
    pass

