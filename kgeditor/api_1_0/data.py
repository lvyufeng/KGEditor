import re
import logging
from . import api
from flask_restx import Resource, fields, reqparse
from kgeditor.dao.data import DataDao
from flask import abort, session, request
from kgeditor.utils.common import login_required

ns = api.namespace("Data", path="/data", description="Graph operations")

data_dao = DataDao()

parser = reqparse.RequestParser()
parser.add_argument('dtype', type=str, default='text')

@ns.route('/')
class DataList(Resource):
    """Shows a list of text data, and lets you to add new text data."""
    @ns.doc('get_data_list')
    @ns.expect(parser)
    @login_required
    def get(self):
        '''List all text data'''
        data = parser.parse_args()
        dtype = data.get('dtype')
        if dtype is None:
            return abort(400, 'Invalid parameters.')
        return data_dao.all(dtype)

    @ns.doc('create_data')
    @login_required
    def post(self):
        """Create new text data"""
        data = api.payload
        return data_dao.create(data)

@ns.route('/<int:id>')
class Data(Resource):
    @ns.doc('delete_data')
    @login_required
    def delete(self, id):
        return data_dao.delete(id)
# @ns.route('/triple')
# class TripleDataList(Resource):
#     """Shows a list of text data, and lets you to add new text data."""
#     @ns.doc('get_text_data_list')
#     @login_required
#     def get(self):
#         '''List all text data'''
#         pass

#     @ns.doc('create_text_data')
#     @login_required
#     def post(self, id):
#         """Create new text data"""
#         pass

