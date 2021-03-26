from flask import Blueprint
api = Blueprint('api_1_0', __name__)
from . import demo, passport, graph, project, domain, data, graph_vertex, graph_edge, model
