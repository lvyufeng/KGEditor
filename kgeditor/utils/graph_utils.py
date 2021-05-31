def exclude_start(visited, start_node):
    excluded = []
    for i in visited:
        if i['_id'] != start_node:
            excluded.append(i)
    return excluded

def process_visited(visited):
    processed = []
    paths = visited['paths']
    for path in paths:
        edges = path['edges']
        if not edges:
            continue
        vertices = path['vertices']
        edge = edges[0]
        # logging.info(vertices)
        edge['_from_name'] = vertices[0]['name'] if vertices[0]['_id'] == edge['_from'] else vertices[1]['name']
        edge['_to_name'] = vertices[0]['name'] if vertices[0]['_id'] == edge['_to'] else vertices[1]['name']
        processed.append(edge)

    return processed