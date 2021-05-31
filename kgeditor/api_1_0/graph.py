from kgeditor.utils.common import login_required
from flask_restx import Resource, fields, reqparse
from . import api
from kgeditor.dao.graph import GraphDAO, VertexDAO
from flask import abort

ns = api.namespace("Graph", path="/graph", description="Graph operations")
graph = api.model(
    "Graph",
    {
        "id": fields.Integer(readonly=True, description="The graph unique identifier"),
    }
)

graph_dao = GraphDAO()
vertex_dao = VertexDAO()

graph_parser = reqparse.RequestParser()
graph_parser.add_argument('domain', type=str)
vertex_praser = reqparse.RequestParser()
vertex_praser.add_argument('page', type=int)
vertex_praser.add_argument('len', type=int)
vertex_like_parser = reqparse.RequestParser()
vertex_like_parser.add_argument('name', type=str)
vertex_like_parser.add_argument('len', type=int)

@ns.route("/")
class GraphList(Resource):
    """Show a list of all graphs, and lets you post to add """
    @ns.doc("list_graphs")
    @ns.expect(graph_parser)
    @login_required
    def get(self):
        """list all graphs"""
        data = graph_parser.parse_args()
        domain_id = data.get('domain')
        if domain_id:
            return graph_dao.all(domain_id=domain_id)
        return graph_dao.all()

    @ns.doc('create_graph')
    @login_required
    def post(self):
        """Create new empty graph"""
        req_dict = api.payload
        name = req_dict.get('name')
        domain_id = req_dict.get('domain_id')
        private = req_dict.get('private')
        if None in [name, domain_id, private]:
            return abort(400, "Invalid parameters.")
        return graph_dao.create(api.payload)    

@ns.route("/<int:graph_id>")
@ns.response(404, 'Graph not found')
@ns.param('id', "The graph identifier")
class Graph(Resource):
    """Show a single graph item and lets you delete them"""
    @ns.doc('get_graph')
    @login_required
    def get(self, graph_id):
        '''Fetch a given resource'''
        return graph_dao.get(graph_id)

    @ns.doc('delete_graph')
    @login_required
    def delete(self, graph_id):
        '''Delete a graph'''
        return graph_dao.delete(graph_id)
        
@ns.route("/<int:graph_id>/traverse")
class GraphTraverse(Resource):
    @ns.doc('traverse_graph')
    @login_required
    def post(self, graph_id):
        '''Fetch a given graph'''
        req_dict = api.payload
        return graph_dao.traverse(graph_id, req_dict)

@ns.route("/<int:graph_id>/neighbor")
class GraphNeighbor(Resource):
    @ns.doc('get_vertex_neighbor')
    @login_required
    def post(self, graph_id):
        '''Fetch a given resource'''
        req_dict = api.payload
        return graph_dao.neighbor(graph_id, req_dict)

@ns.route("/<int:graph_id>/vertex/<string:collection>")
@ns.response(404, 'Graph not found')
@ns.param('id', "The graph identifier")
class VertexList(Resource):
    """Show a single graph item and lets you delete them"""
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