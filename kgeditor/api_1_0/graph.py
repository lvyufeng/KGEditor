from kgeditor.utils.common import login_required
from flask_restx import Resource, fields, reqparse
from . import api
from kgeditor.dao.graph import GraphDAO
from flask import abort

ns = api.namespace("Graph", path="/graph", description="Graph operations")
graph = api.model(
    "Graph",
    {
        "id": fields.Integer(readonly=True, description="The graph unique identifier"),
    }
)

graph_dao = GraphDAO()

graph_parser = reqparse.RequestParser()
graph_parser.add_argument('domain', type=str)

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