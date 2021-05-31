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

@ns.route("/<int:id>")
@ns.response(404, 'Graph not found')
@ns.param('id', "The graph identifier")
class Graph(Resource):
    """Show a single graph item and lets you delete them"""
    @ns.doc('get_graph')
    @login_required
    def get(self, id):
        '''Fetch a given resource'''
        return graph_dao.get(id)

@ns.route("/<int:id>/traverse")
class GraphTraverse(Resource):
    @ns.doc('traverse_graph')
    @login_required
    def post(self, id):
        '''Fetch a given resource'''
        req_dict = api.payload
        return graph_dao.traverse(id, req_dict)

@ns.route("/<int:id>/neighbor")
class GraphNeighbor(Resource):
    @ns.doc('get_vertex_neighbor')
    @login_required
    def post(self, id):
        '''Fetch a given resource'''
        req_dict = api.payload
        return graph_dao.neighbor(id, req_dict)

@ns.route("/<int:id>/vertex/<string:collection>")
@ns.response(404, 'Graph not found')
@ns.param('id', "The graph identifier")
class VertexList(Resource):
    """Show a single graph item and lets you delete them"""
    @ns.doc('get_graph_vertex')
    @ns.expect(vertex_praser)
    @login_required
    def get(self, id, collection):
        '''Fetch a given vetex collection'''
        data = vertex_praser.parse_args()
        page = data.get('page')
        page_len = data.get('len')
        if None in [page, page_len]:
            return abort(400, "Invalid parameters.")
        return vertex_dao.get(collection, page, page_len)

    @ns.doc('create_graph_vertex')
    @login_required
    def post(self, id, collection):
        '''Create a new vertex'''
        req_dict = api.payload
        name = req_dict.get('name')
        if not name:
            return abort(400, "Invalid parameters.")
        return vertex_dao.create(id, collection, api.payload)

@ns.route('/<int:graph_id>/vertex/<string:collection>/<string:vertex_id>')
class Vertex(Resource):
    """Show a single vertex item and lets you delete them"""
    @ns.doc('delete_vertex')
    @login_required
    def delete(self, graph_id, collection, vertex_id):
        '''Delete a task given its identifier.'''
        return vertex_dao.delete(graph_id, collection, vertex_id)