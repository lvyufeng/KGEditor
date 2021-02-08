@api.route('/link', methods=['POST'])
@login_required
def link():
    """连接Node
    A shorthand for createEdge that takes two documents as input
    
    Args:
        link_type:
        from:
        to:
        attributes:
    """
    graph_id = session.get('graph_id')
    domain_id = session.get('domain_id')
    if not all([graph_id, domain_id]):
        return jsonify(errno=RET.SESSIONERR, errmsg="未选择指定的图谱")
    logging.info(graph_id)
    logging.info(domain_id)
    domain_db = arango_conn['domain_{}'.format(domain_id)]
    db_graph = domain_db.graphs['graph_{}'.format(graph_id)]
    req_dict = request.get_json()
    link_type = req_dict.pop('link_type')
    doc1 = req_dict.get('from')
    doc2 = req_dict.get('to')
    attributes = req_dict.get('attributes')
    logging.info(req_dict)
    # logging.info()
    try:
        data = db_graph.link(link_type, doc1, doc2, attributes)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="添加连接失败")
    return jsonify(errno=RET.OK, errmsg="OK")