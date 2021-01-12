import redis
class Config(object):
    """
    config setting info
    """
    DEBUG = True
    SECRET_KEY = "this_is_a_secret_key"
    # db
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = '3306'
    MYSQL_USER_NAME = 'root'
    MYSQL_PASSWD = 'password'
    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}:{}/KGEditor'.format(MYSQL_USER_NAME, MYSQL_PASSWD, MYSQL_HOST, MYSQL_PASSWD)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # redis
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    # flask-session
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True #hidden cookie session_id
    PERMANENT_SESSION_LIFETIME = 86400

    # neo4j
    NEO4J_HOST = 'localhost'
    NEO4J_PORT = '7687'
    NEO4J_PASSWD = 'password'
    NEO4J_ENCODING = 'utf-8'

class DevelopmentConfig(Config):
    """
    Dev environment
    """
    DEBUG = True

class ProductionConfig(Config):
    """
    Product environment
    """

config_map = {
    'develop':DevelopmentConfig,
    'product':ProductionConfig
}