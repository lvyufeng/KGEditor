from flask_restx import Resource, fields
from . import api

ns = api.namespace("Graph", path="/graph", description="Graph operations")
graph = api.model(
    "Graph",
    {
        "id": fields.Integer(readonly=True, description="The graph unique identifier"),
    }
)

@ns.route("/")
class GraphList(Resource):
    """Show a list of all graphs, and lets you post to add """
    @ns.doc("list_graphs")
    @ns.marshal_list_with(graph)
    def get(self):
        """list all graphs"""
        return []

# @ns.route("/<int:id>")
# @ns.response(404, 'Graph not found')
# @ns.param('id', "The graph identifier")
# class Graph(Resource):
#     """"""