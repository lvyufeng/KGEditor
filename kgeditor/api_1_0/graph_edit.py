from . import api
from flask import jsonify, g, request, session
from kgeditor.utils.common import login_required, verify_graph
from kgeditor import db, arango_conn
from kgeditor.models import Graph
from kgeditor.utils.response_code import RET
from sqlalchemy.exc import IntegrityError
import logging
from pyArango.consts import *

@api.route('add_entity_type', methods=['POST'])
@login_required
@verify_graph
def list_documents():
    documents = []
    graph_db = arango_conn['graph_{}'.format(g.graph_id)]
    
    for name, collection in graph_db.collections.items():
        if collection.type == COLLECTION_DOCUMENT_TYPE and not name.startswith('_'):
            documents.append(name)
    return jsonify(errno=RET.OK, errmsg="OK", data=documents)