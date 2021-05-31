from flask_restx import Resource, fields, reqparse
from . import api
from kgeditor.dao.project import ProjectDAO
from flask import abort, session, request
import re
import logging
from kgeditor.utils.common import login_required
from kgeditor.constants import TASK_ANNOTATION, TASK_FUSION, TASK_GRAPH

ns = api.namespace('Project', path='/', description='Project operations')

project_dao = ProjectDAO()

parser = reqparse.RequestParser()
parser.add_argument('type', type=str)

@ns.route('/project')
class ProjectList(Resource):
    """Shows a list of all projects, and lets you to add new projects."""
    @ns.doc('list_projects')
    @ns.expect(parser)
    @login_required
    def get(self):
        '''List all projects'''
        data = parser.parse_args()
        project_type = data.get('type')
        if project_type == '0':
            return project_dao.all(project_type=TASK_ANNOTATION)
        elif project_type == '1':
            return project_dao.all(project_type=TASK_FUSION)
        return project_dao.all()

    @ns.doc('create_project')
    @login_required
    def post(self):
        """Create new project"""
        req_dict = api.payload
        name = req_dict.get('name')
        if not name:
            return abort(400, "Invalid parameters.")
        return project_dao.create(api.payload)

@ns.route('/project/<int:id>')
class Project(Resource):
    """Show a single project item and lets you delete them"""
    @ns.doc('get_project')
    @login_required
    def get(self, id):
        '''Fetch a given resource'''
        return project_dao.get(id)

    @ns.doc('delete_project')
    @login_required
    def delete(self, id):
        '''Delete a project'''
        return project_dao.delete(id)

@ns.route('/project/<int:id>/task')
class ProjectTask(Resource):
    """Commit the task of project and get the status of it"""
    @ns.doc('commit_project')
    @login_required
    def post(self, id):
        """Commit the task"""
        return [], 201

    @ns.doc('get_status')
    def get(self, id):
        """Fetch the status of task"""
        return [], 200   
