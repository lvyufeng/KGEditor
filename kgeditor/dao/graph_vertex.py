import json
import logging
from kgeditor import domain_db
from flask import abort
from pyArango.query import AQLQuery

class VertexDAO:
    def __init__(self):
        pass

    def get(self, id):
        pass

    def create(self, graph_id, collection, data):
        db_graph = domain_db.graphs['graph_{}'.format(graph_id)]
        try:
            vertex = db_graph.createVertex(collection, data)
        except Exception as e:
            logging.error(e)
            return abort(500, 'Create vertex failed.')
        return {'message':'Create vertex succeed.', 'id': vertex._id}, 201

    def update(self, graph_id, collection, vertex_id, data):
        db_graph = domain_db.graphs['graph_{}'.format(graph_id)]
        url = "%s/vertex/%s/%s" % (db_graph.getURL(), collection, vertex_id)
        try:
            r = db_graph.connection.session.patch(url, data = json.dumps(data, default=str))        
        except Exception as e:
            logging.error(e)
            return abort(500, 'Database error.')
        if r.status_code == 200 or r.status_code == 202:
            return {'message':'Updata vertex succeed.'}, 200
        return abort(500, 'Database error.')

    def delete(self, graph_id, collection, vertex_id):
        db_graph = domain_db.graphs['graph_{}'.format(graph_id)]
        try:
            document = domain_db[collection][vertex_id]
            db_graph.deleteVertex(document)
        except Exception as e:
            logging.error(e)
            return abort(500, 'Database error.')
        return  {'message':'Delete vertex succeed.'}, 200

    def all(self, id, page, page_len):
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

    def like(self, graph_id, name, batch_len):
        db_graph = domain_db.graphs['graph_{}'.format(graph_id)]
        collections = []
        for k, v in db_graph.definitions.items():
            collections.extend(v.fromCollections)
            collections.extend(v.toCollections)
        collections = list(set(collections))
        collections.extend(db_graph._orphanedCollections)
        logging.info(collections)
        # use CONTAINS instead of LIKE to improve the performance
        aql = "FOR vertex IN {} \
                    FILTER CONTAINS(vertex.name, '{}') \
                    RETURN vertex"
        fuzzy_result = []
        for collection in collections:
            try:
                query = AQLQuery(domain_db, aql.format(collection, name), int(batch_len/len(collections)), {}, {}, False, False)
            except Exception as e:
                logging.error(e)
                return abort(500, 'Database error.')
            fuzzy_result.extend([{'_id': i['_id'], 'value': i['name']} for i in query])

        return {'data':fuzzy_result, 'message':'Fetch fuzzy vertex succeed.'}, 200