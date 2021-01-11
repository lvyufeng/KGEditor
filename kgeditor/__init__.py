import redis
import logging
import pymysql

from flask import Flask
from config import config_map
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect
from logging.handlers import RotatingFileHandler
from  py2neo import Graph
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
graph = None

def create_app(mode):
    """
    create app
    """
    app = Flask(__name__)
    config_cls = config_map.get(mode)
    app.config.from_object(config_cls)

    # init db
    db.init_app(app)

    # init redis
    global redis_store
    redis_store = redis.StrictRedis(host=config_cls.REDIS_HOST, port=config_cls.REDIS_PORT)

    global graph
    # graph = 
    # flask session, store session in redis
    Session(app)

    # csrf protection
    # CSRFProtect(app)

    from kgeditor import api_1_0
    app.register_blueprint(api_1_0.api, url_prefix="/api/v1.0")
    return app