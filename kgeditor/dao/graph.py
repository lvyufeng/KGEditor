from kgeditor.models import Graph
from flask import session, abort, g
import logging
from kgeditor import domain_db, db

class GraphDAO:
    def __init__(self):
        pass

    def get(self, id):
        try:
            graph = domain_db.graphs['graph_{}'.format(id)]
        except:
            abort(500, 'Database error.')
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
            graph = Graph.query.filter_by(name=data['name']).first()
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

    def delete(self, id):
        pass

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

class VertexDAO:
    def __init__(self):
        pass

    def get(self, id, page, page_len):
        try:
            page = int(page)
            page_len = int(page_len)
            collection = domain_db.collections[id]
        except Exception as e:
            logging.error(e)
            return abort(500, 'Database error.')

        if page < 1:
            return abort(500, 'Page count error.')
        count = collection.count()
        if page_len * (page - 1) > count:
            return abort(500, 'Database error.')
        data = collection.fetchAll(limit = page_len, skip = page_len * (page - 1))
        pages = int(count / page_len) + 1

        return {'data':{'vertex': data.result, 'pages': pages, 'count':count}, 'message':'Fetch vertex succeed.'}, 200

    def create(self, data):
        pass

    def update(self, id, data):
        pass

    def delete(self, id):
        pass

class EdgeDAO:
    def __init__(self):
        pass

    def get(self, id):
        pass

    def create(self, data):
        pass

    def update(self, id, data):
        pass

    def delete(self, id):
        pass