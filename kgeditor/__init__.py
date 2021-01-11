import redis
import logging
import pymysql

from flask import Flask
from flask_cors import CORS
from config import config_map
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect
from logging.handlers import RotatingFileHandler
from py2neo import Graph, GraphService
pymysql.install_as_MySQLdb()

# set log level
logging.basicConfig(level=logging.DEBUG)
# create log handler
file_log_handler = RotatingFileHandler('logs/log',maxBytes=1024*1024*100, backupCount=10)
# create log formatter
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# set formatter
file_log_handler.setFormatter(formatter)
# global logger
logging.getLogger().addHandler(file_log_handler)

db = SQLAlchemy()
redis_store = None
neo4j = None

def create_app(mode):
    """
    create app
    """
    app = Flask(__name__)
    config_cls = config_map.get(mode)
    app.config.from_object(config_cls)

    # cross domain
    CORS(app, supports_credentials=True)
    # init db
    db.init_app(app)

    # init redis
    global redis_store
    redis_store = redis.StrictRedis(host=config_cls.REDIS_HOST, port=config_cls.REDIS_PORT)

    global neo4j
    # neo4j = Graph(host=config_cls.NEO4J_HOST, port=config_cls.NEO4J_PORT, password=config_cls.NEO4J_PASSWD, encoding=config_cls.NEO4J_ENCODING)
    neo4j = GraphService("bolt://{}:{}".format(config_cls.NEO4J_HOST, config_cls.NEO4J_PORT), password=config_cls.NEO4J_PASSWD)
    # flask session, store session in redis
    Session(app)

    # csrf protection
    # CSRFProtect(app)

    from kgeditor import api_1_0
    app.register_blueprint(api_1_0.api, url_prefix="/api/v1.0")
    return app