import json
import logging
from kgeditor import domain_db
from flask import abort
from pyArango.query import AQLQuery


class EdgeDAO:
    def __init__(self):
        pass

    def get(self, graph_id, collection, edge_id):
        db_graph = domain_db.graphs['graph_{}'.format(graph_id)]
        url = "%s/edge/%s/%s" % (db_graph.getURL(), collection, edge_id)

        try:
            r = db_graph.connection.session.get(url)        
        except Exception as e:
            logging.error(e)
            return abort(500, 'Database error.')
        if r.status_code == 200:
            data = r.json()
            return {'data':data['edge'],'message':'Fetch edge succeed.'}, 200
        return abort(500, 'Database error.')

    def create(self, graph_id, collection, req):
        db_graph = domain_db.graphs['graph_{}'.format(graph_id)]

        try:
            db_graph.createEdge(collection, req['from'], req['to'], req['attribute'])
        except Exception as e:
            logging.error(e)
            return abort(500, 'Database error.')
        return {'message':'Create edge succeed.'}, 201


    def update(self, graph_id, collection, edge_id, new_collection):
        edge_data, status = self.get(graph_id, collection, edge_id)
        if status != 200:
            return abort(500, 'Database error.')
        req_dict = {
            'from':edge_data['data']['_from'],
            'to':edge_data['data']['_to'],
            'attribute':{}
        }
        _, status = self.create(graph_id, new_collection, req_dict)
        self.delete(graph_id, collection, edge_id)
        if status != 201:
            return abort(500, 'Database error.')
        return {'message':'Update edge succeed.'}, 200

    def delete(self, graph_id, collection, edge_id):
        db_graph = domain_db.graphs['graph_{}'.format(graph_id)]

        try:
            document = domain_db[collection][edge_id]
            db_graph.deleteEdge(document)
        except Exception as e:
            logging.error(e)
            return abort(500, 'Database error.')
        return {'message':'Delete edge succeed.'}, 200
