import re
import logging
from . import api
from flask_restx import Resource, fields
from kgeditor.dao.data import DataDao
from flask import abort, session, request
from kgeditor.utils.common import login_required

ns = api.namespace("Data", path="/data", description="Graph operations")

data_dao = DataDao()

@ns.route('/text')
class TextDataList(Resource):
    """Shows a list of text data, and lets you to add new text data."""
    @ns.doc('get_text_data_list')
    @login_required
    def get(self):
        '''List all text data'''
        pass

    @ns.doc('create_text_data')
    @login_required
    def post(self, id):
        """Create new text data"""
        pass
