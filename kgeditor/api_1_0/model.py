from flask_restx import Resource, fields
from . import api
from kgeditor.dao.model import ModelDAO
from flask import abort, session, request
import re
import logging
from kgeditor.utils.common import login_required

ns = api.namespace('Model', path='/', description='Model operations')

model_dao = ModelDAO()

@ns.route('/model')
class ModelList(Resource):
    """Shows a list of all models, and lets you to add new models."""
    @ns.doc('list_models')
    @login_required
    def get(self):
        '''List all models'''
        return model_dao.all()

    @ns.doc('add_model')
    @login_required
    def post(self):
        req_dict = api.payload
        name = req_dict.get('name')
        model_type = req_dict.get('type')
        url = req_dict.get('url')
        private = req_dict.get('private')
        if None in [name, url, model_type, private]:
            return abort(400, "Invalid parameters.")
        return model_dao.create(api.payload)

@ns.route('/model/annotation')
class AnnotationModelList(Resource):
    """Shows a list of all annotation models"""
    @ns.doc('list_annotation_models')
    @login_required
    def get(self):
        '''List all models'''
        return model_dao.all(0)

@ns.route('/model/fusion')
class FusionModelList(Resource):
    """Shows a list of all fusion models"""
    @ns.doc('list_fusion_models')
    @login_required
    def get(self):
        '''List all models'''
        return model_dao.all(1)

@ns.route('/model/<int:id>')
@ns.response(404, 'Model not found.')
@ns.param('id', 'The model identifier.')
class Model(Resource):
    """Show a single model item and lets you delete them"""
    @ns.doc('get_model')
    @login_required
    def get(self, id):
        '''Fetch a given resource'''
        return model_dao.get(id)
    
    @ns.doc('update_model')
    @login_required
    def patch(self, id):
        '''Update a model given its identifier.'''
        req_dict = api.payload
        name = req_dict.get('name')
        model_type = req_dict.get('type')
        url = req_dict.get('url')
        private = req_dict.get('private')
        if None in [name, url, model_type, private]:
            return abort(400, "Invalid parameters.")
        
        return model_dao.update(id, api.payload)

    @ns.doc('delete_model')
    @login_required
    def delete(self, id):
        '''Delete a model given its identifier.'''
        return model_dao.delete(id)