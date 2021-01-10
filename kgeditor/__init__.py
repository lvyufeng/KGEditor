from flask import Flask
from config import config_map
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect
from kgeditor import api_1_0
import redis

db = SQLAlchemy()
redis_store = None

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

    # flask session, store session in redis
    Session(app)

    # csrf protection
    CSRFProtect(app)
    app.register_blueprint(api_1_0.api, url_prefix="/api/v1.0")
    return app