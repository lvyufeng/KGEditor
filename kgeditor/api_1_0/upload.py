import logging
from . import api
from flask import abort
from flask_restx import Resource
from kgeditor import data, text
from kgeditor.utils.common import login_required
from werkzeug.datastructures import FileStorage

dtype_dict = {
    'text': text,
    'data': data
}

ns = api.namespace('Data', path='/', description='Upload operations')
upload_parser = ns.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)

@ns.route('/upload/<string:dtype>')
@ns.expect(upload_parser)
class Upload(Resource):
    """Upload a file like txt or csv"""
    @ns.doc('upload_file')
    @login_required
    def post(self, dtype):
        """Upload file to server"""
        args = upload_parser.parse_args()
        uploaded_file = args['file']  # This is FileStorage instance
        try:
            file_name = dtype_dict.get(dtype).save(uploaded_file)
            logging.info(file_name)
        except Exception as e:
            logging.error(e)
            return abort(500, 'Upload file failed.')
        return {'message': 'Upload file succeed.', 'url': file_name}, 201