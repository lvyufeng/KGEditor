from . import api
from kgeditor.utils.common import login_required
from kgeditor.dao.graph_edge import EdgeDAO
from flask import abort
from flask_restx import Resource, fields, reqparse

ns = api.namespace("Graph", path="/graph", description="Graph operations")

edge_dao = EdgeDAO()

@ns.route('/<int:graph_id>/edge/<string:collection>')
class EdgeList(Resource):
    ''''''
    @ns.doc('create_graph_edge')
    @login_required
    def post(self, graph_id, collection):
        '''Create a new edge'''
        req_dict = api.payload
        _from = req_dict.get('from')
        _to = req_dict.get('to')
        attribute = req_dict.get('attribute')

        if None in [_from, _to, attribute]:
            return abort(400, "Invalid parameters.")
        
        return edge_dao.create(graph_id, collection, req_dict)

@ns.route('/<int:graph_id>/edge/<string:collection>/<edge_id>')
class Edge(Resource):
    @ns.doc('get_graph_edge')
    def get(self, graph_id, collection, edge_id):
        '''Show a graph edge and lets you delete it.'''
        return edge_dao.get(graph_id, collection, edge_id)

    @ns.doc('delete_graph_edge')
    def delete(self, graph_id, collection, edge_id):
        '''Show a graph edge and lets you delete it.'''
        return edge_dao.delete(graph_id, collection, edge_id)

    @ns.doc('update_graph_edge')
    def patch(self, graph_id, collection, edge_id):
        '''Update graph edge'''
        req_dict = api.payload
        new_collection = req_dict.get('relation')
        if new_collection is None:
            return abort(400, 'Invalid parameters.')
        return edge_dao.update(graph_id, collection, edge_id, new_collection)