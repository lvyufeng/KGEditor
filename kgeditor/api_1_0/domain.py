from flask_restx import Resource, fields
from . import api
from kgeditor.dao.domain import DomainDAO
from flask import abort, session, request
import re
import logging
from kgeditor.utils.common import login_required

ns = api.namespace('Domain', path='/', description='Domain operations')

domain_dao = DomainDAO()


@ns.route('/domain')
class DomainList(Resource):
    """Shows a list of all domains, and lets you to add new domains."""
    @ns.doc('list_domains')
    @login_required
    def get(self):
        '''List all domains'''
        return domain_dao.all

    @ns.doc('create_domain')
    @login_required
    def post(self):
        """Create new domain"""
        req_dict = api.payload
        name = req_dict.get('name')
        if not name:
            return abort(400, "Invalid parameters.")
        return domain_dao.create(api.payload)

@ns.route('/domain/<int:id>')
@ns.response(404, 'Domain not found.')
@ns.param('id', 'The domain identifier.')
class Domain(Resource):
    """Show a single domain item and lets you delete them"""
    @ns.doc('get_domain')
    @login_required
    def get(self, id):
        '''Fetch a given resource'''
        return domain_dao.get(id)
    
    @ns.doc('update_domain')
    @login_required
    def patch(self, id):
        '''Update a task given its identifier.'''
        req_dict = api.payload
        name = req_dict.get('name')
        if not name:
            return abort(400, "Invalid parameters.")
    
        return domain_dao.update(id, api.payload)

    @ns.doc('delete_domain')
    @login_required
    def delete(self, id):
        '''Delete a task given its identifier.'''
        return domain_dao.delete(id)