import re
import logging
from flask_restx import Resource, fields, reqparse
from . import api
from kgeditor.dao.project import ProjectDAO
from flask import abort, session, request
from kgeditor.utils.common import login_required
from kgeditor.constants import TASK_ANNOTATION, TASK_FUSION, TASK_GRAPH
from tasks.test_task.tasks import long_task

ns = api.namespace('Project', path='/', description='Project operations')

project_dao = ProjectDAO()

parser = reqparse.RequestParser()
parser.add_argument('type', type=str)
task_parser = reqparse.RequestParser()
task_parser.add_argument('task_id', type=str)

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
        if project_type == 'annotation':
            return project_dao.all(project_type=TASK_ANNOTATION)
        elif project_type == 'fusion':
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

    @ns.doc('update_project')
    @login_required
    def patch(self, id):
        '''Update project'''
        req_dict = api.payload
        name = req_dict.get('name')
        if not name:
            return abort(400, "Invalid parameters.")
        return project_dao.update(id, req_dict)

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
        task = long_task.apply_async()
        return {'data': {'task_id':task.id}}, 201

    @ns.doc('get_status')
    @ns.expect(task_parser)
    def get(self, id):
        """Fetch the status of task"""
        data = task_parser.parse_args()
        task_id = data.get('task_id')
        if task_id is None:
            return abort(400, 'Invalid parameters.')
        task = long_task.AsyncResult(task_id)
        if task.state == 'PENDING':
            # job did not start yet
            response = {
                'state': task.state,
                'current': 0,
                'total': 1,
                'status': 'Pending...'
            }
        elif task.state != 'FAILURE':
            response = {
                'state': task.state,
                'current': task.info.get('current', 0),
                'total': task.info.get('total', 1),
                'status': task.info.get('status', '')
            }
            if 'result' in task.info:
                response['result'] = task.info['result']
        else:
            # something went wrong in the background job
            response = {
                'state': task.state,
                'current': 1,
                'total': 1,
                'status': str(task.info),  # this is the exception raised
            }
        return {'data':response}, 200   
