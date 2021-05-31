import logging
from kgeditor.models import Graph
from kgeditor import domain_db, db
from kgeditor.utils.graph_utils import process_visited
from flask import session, abort, g

class GraphDAO:
    def __init__(self):
        pass

    def get(self, id):
        try:
            graph = domain_db.graphs['graph_{}'.format(id)]
        except Exception as e:
            return abort(500, 'Database error.')
        collections = []
        edges = []
        for k, v in graph.definitions.items():
            edges.append(k)
            collections.extend(v.fromCollections)
            collections.extend(v.toCollections)
        collections = list(set(collections))
        collections.extend(graph._orphanedCollections)
        return {'data':{'collections': collections, 'edges':edges}, 'message':'Fetch graph succeed.'}, 200

    def create(self, data):
        user_id = g.user_id
        try:
            graph = Graph.query.filter_by(name=data['name'], creator_id=user_id).first()
        except Exception as e:
            logging.error(e)
            return abort(500, 'Database error.')
        else:
            if graph is not None:
                return abort(500, 'Graph already exist.')
        # 5.save graph info to db
        graph = Graph(name=data['name'], private=data['private'], creator_id=user_id, domain_id=data['domain_id'], connected=False)
        try:
            db.session.add(graph)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return abort(500, 'Database error.')
        
        return {'message': 'Create graph succeed.'}, 201


    def update(self, id, data):
        pass

    def delete(self, graph_id):
        user_id = g.user_id
        try:
            graph = Graph.query.filter_by(id=graph_id, creator_id=user_id).first()
        except Exception as e:
            logging.error(e)
            return abort(500, 'Database error.')
        else:
            if graph is None:
                return abort(500, 'Graph not exist.')
        if graph.connected:
            try:
                db.session.delete(graph)
                db.session.commit()
                g_graph = domain_db.graphs['graph_{}'.format(graph_id)]
                g_graph.delete()
            except Exception as e:
                logging.error(e)
                db.session.rollback()
                return abort(500, 'Database error.')
        else:
            try:
                db.session.delete(graph)
                db.session.commit()
            except Exception as e:
                logging.error(e)
                db.session.rollback()
                return abort(500, 'Database error.')
        return {'message': 'Delete graph succeed.'}, 200

    def all(self, domain_id=None):
        user_id = session.get('user_id')
        try:
            if domain_id is None:
                graph_list = Graph.query.filter_by(creator_id=user_id).all()
            else:
                graph_list = Graph.query.filter_by(creator_id=user_id, domain_id=domain_id).all()
        except Exception as e:
            logging.error(e)
            return abort(500, 'Database error.')
        graph_dict_list = []
        for graph in graph_list:
            graph_dict_list.append(graph.to_dict())

        return {'data': graph_dict_list, 'message': 'Query succeed.'}, 200

    def traverse(self, graph_id, req_dict):
        db_graph = domain_db.graphs['graph_{}'.format(graph_id)]
        startVertex = req_dict.pop('startVertex')
        try:
            data = db_graph.traverse(startVertex, **req_dict)
        except Exception as e:
            logging.error(e)
            return abort(500, 'Database error.')

        return {'data':data['visited'], 'message':'Traverse knowledge graph succeed.'}, 200

    def neighbor(self, graph_id, req_dict):
        db_graph = domain_db.graphs['graph_{}'.format(graph_id)]
        startVertex = req_dict.get('startVertex')

        try:
            data = db_graph.traverse(startVertex, direction='any', maxDepth=1, minDepth=0)
        except Exception as e:
            logging.error(e)
            return abort(500, 'Database error.')

        return {'data':process_visited(data['visited']), 'message':'Fetch vertex neighbor succeed.'}, 200
