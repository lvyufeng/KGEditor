from flask import Blueprint
from flask_restx import Api

api_v1 = Blueprint('api_1_0', __name__)
api = Api(api_v1, version="1.0", title="KGEditor API", description="KGEditor Restful API")

# from . import demo, passport, project, domain, data, model
# from .graph import graph, graph_edge, graph_vertex
# from .project import project, annotation_project, fusion_project
from .graph import *
from .passport import *
from .domain import *
from .project import *
