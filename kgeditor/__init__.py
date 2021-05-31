import redis
import logging
import pymysql
from flask import Flask
from flask_cors import CORS
from config import config_map
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect
from flask_uploads import DATA, UploadSet, configure_uploads, patch_request_class, TEXT
from flask_docs import ApiDoc
from logging.handlers import RotatingFileHandler
from pyArango.connection import *
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
domain_db = None
text = UploadSet('data', TEXT)
data = UploadSet('data', DATA)
file_path = None

def create_app(mode):
    """
    create app
    """
    app = Flask(__name__)
    config_cls = config_map.get(mode)
    app.config.from_object(config_cls)

    global file_path
    file_path = config_cls.UPLOADED_DATA_DEST

    # cross domain
    CORS(app, supports_credentials=True)
    # init db
    db.init_app(app)

    # init redis
    global redis_store
    redis_store = redis.StrictRedis(host=config_cls.REDIS_HOST, port=config_cls.REDIS_PORT)

    global domain_db
    arango_conn = Connection(config_cls.ARANGO_URL, username=config_cls.ARANGO_USERNAME, password=config_cls.ARANGO_PASSWORD)
    domain_db = arango_conn['domain_27']

    # flask session, store session in redis
    Session(app)

    # csrf protection
    # CSRFProtect(app)

    # configure uploads
    
    configure_uploads(app, data)
    configure_uploads(app, text)
    patch_request_class(app)

    ApiDoc(app)
    from kgeditor import api_1_0
    app.register_blueprint(api_1_0.api_v1, url_prefix="/api/v1.0")
    return app