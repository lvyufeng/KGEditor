from flask_restx import Resource, fields
from . import api
from kgeditor.dao.project import ProjectDAO
from flask import abort, session, request
import re
import logging
from kgeditor.utils.common import login_required
from kgeditor.constants import TASK_ANNOTATION, TASK_FUSION, TASK_GRAPH
from werkzeug.datastructures import FileStorage

ns = api.namespace('Upload', path='/', description='Upload operations')
upload_parser = ns.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)
@ns.route('/upload/')
@ns.expect(upload_parser)
class Upload(Resource):
    def post(self):
        args = upload_parser.parse_args()
        uploaded_file = args['file']  # This is FileStorage instance
        url = do_something_with_file(uploaded_file)
        return {'url': url}, 201