"""
entity and relation types are defined as collection in ArangoDB,
and all operations of them are assigned in this file
"""
from . import api
from flask import jsonify, g, request, session
from kgeditor.utils.common import login_required, verify_graph
from kgeditor import db, arango_conn
from kgeditor.models import Graph
from kgeditor.utils.response_code import RET
from sqlalchemy.exc import IntegrityError
import logging
from pyArango.consts import *

@api.route('list_documents', methods=['POST'])
@login_required
@verify_graph
def list_documents():
    documents = []
    graph_db = arango_conn['graph_{}'.format(g.graph_id)]
    
    for name, collection in graph_db.collections.items():
        if collection.type == COLLECTION_DOCUMENT_TYPE and not name.startswith('_'):
            documents.append(name)
    return jsonify(errno=RET.OK, errmsg="OK", data=documents)

@api.route('list_edges', methods=['POST'])
@login_required
@verify_graph
def list_edges():
    graph_db = arango_conn['graph_{}'.format(g.graph_id)]
    # graph_db.collections
    edges = []
    for name, collection in graph_db.collections.items():
        if collection.type == COLLECTION_EDGE_TYPE:
            edges.append(name)
    # logging.info(graph_db.collections)
    return jsonify(errno=RET.OK, errmsg="OK", data=edges)

