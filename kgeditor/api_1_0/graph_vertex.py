from kgeditor.utils.common import login_required
from flask_restx import Resource, reqparse
from . import api
from kgeditor.dao.graph_vertex import VertexDAO
from flask import abort

ns = api.namespace("Graph", path="/graph", description="Graph operations")

vertex_dao = VertexDAO()

vertex_praser = reqparse.RequestParser()
vertex_praser.add_argument('page', type=int)
vertex_praser.add_argument('len', type=int)
vertex_like_parser = reqparse.RequestParser()
vertex_like_parser.add_argument('name', type=str)
vertex_like_parser.add_argument('len', type=int)

@ns.route("/<int:graph_id>/vertex/<string:collection>")
@ns.response(404, 'Graph not found')
@ns.param('id', "The graph identifier")
class VertexList(Resource):
    @ns.doc('get_graph_vertex')
    @ns.expect(vertex_praser)
    @login_required
    def get(self, graph_id, collection):
        '''Fetch a given vetex collection'''
        data = vertex_praser.parse_args()
        page = data.get('page')
        page_len = data.get('len')
        if None in [page, page_len]:
            return abort(400, "Invalid parameters.")
        return vertex_dao.all(collection, page, page_len)

    @ns.doc('create_graph_vertex')
    @login_required
    def post(self, graph_id, collection):
        '''Create a new vertex'''
        req_dict = api.payload
        name = req_dict.get('name')
        if not name:
            return abort(400, "Invalid parameters.")
        return vertex_dao.create(graph_id, collection, api.payload)

@ns.route('/<int:graph_id>/vertex/<string:collection>/<string:vertex_id>')
class Vertex(Resource):
    """Show a single vertex item and lets you delete them"""
    @ns.doc('delete_vertex')
    @login_required
    def delete(self, graph_id, collection, vertex_id):
        '''Delete a vetex given its identifier.'''
        return vertex_dao.delete(graph_id, collection, vertex_id)

    @ns.doc('update_vetex')
    @login_required
    def patch(self, graph_id, collection, vertex_id):
        '''Update a vetex given its identifier.'''
        req_dict = api.payload
        name = req_dict.get('name')
        if not name:
            return abort(400, "Invalid parameters.")
    
        return vertex_dao.update(graph_id, collection, vertex_id, api.payload)

@ns.route("/<int:graph_id>/vertex/like")
class VertexLike(Resource):
    """Show a single graph item and lets you delete them"""
    @ns.doc('get_graph_vertex')
    @ns.expect(vertex_like_parser)
    @login_required
    def get(self, graph_id):
        '''Fetch a given vetex collection'''
        data = vertex_like_parser.parse_args()
        name = data.get('name')
        batch_len = data.get('len')
        if None in [name, len]:
            return abort(400, "Invalid parameters.")
        return vertex_dao.like(graph_id, name, batch_len)