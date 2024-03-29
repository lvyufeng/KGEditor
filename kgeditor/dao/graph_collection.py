import json
import logging
from kgeditor import domain_db
from flask import abort
from pyArango.query import AQLQuery

class CollectionDAO:
    def __init__(self):
        pass

    def get(self, graph_id, type):
        if type not in ['edge', 'vertex']:
            return abort(500, 'Database error.')

        db_graph = domain_db.graphs['graph_{}'.format(graph_id)]
        url = "%s/%s" % (db_graph.getURL(), type)

        try:
            r = db_graph.connection.session.get(url)        
        except Exception as e:
            logging.error(e)
            return abort(500, 'Database error.')
        if r.status_code == 200:
            data = r.json()
            return {'data':data['collections'],'message':'Fetch edge succeed.'}, 200
        return abort(500, 'Database error.')

    def create(self, graph_id, type, req):
        if type not in ['edge', 'vertex']:
            return abort(500, 'Database error.')

        db_graph = domain_db.graphs['graph_{}'.format(graph_id)]
        if type == 'vertex':
            collection_type = 'Collection' 
            url = "%s/vertex" % (db_graph.getURL())

            data = { 
                    "collection" : req['name'] 
                }
        else:
            collection_type = 'Edges' 
            url = "%s/edge" % (db_graph.getURL())
            data = { 
                "collection" : req['name'], 
                "from" : req['from'], 
                "to" : req['to'] 
            }
        try:
            domain_db.createCollection(collection_type, name=req['name'])
        except Exception as e:
            logging.error(e)
            if 'already has a collection' in e.message:
                pass
            else:       
                return abort(500, 'Database error.')
        

        try:
            print(url)
            r = db_graph.connection.session.post(url, json=data)
            print(r)        
        except Exception as e:
            logging.error(e)
            return abort(500, 'Database error.')

        return {'message': f'Create {type} collection succeed.'}, 201
