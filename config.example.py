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
    MYSQL_USERNAME = 'root'
    MYSQL_PASSWORD = 'password'
    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}:{}/KGEditor'.format(MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # redis
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    # flask-session
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True #hidden cookie session_id
    PERMANENT_SESSION_LIFETIME = 86400

    # ArangoDB
    ARANGO_URL = 'http://localhost:8529'
    ARANGO_USERNAME = 'root'
    ARANGO_PASSWORD = 'password'

    # uploads
    UPLOADED_DATA_DEST = '/tmp/'
    UPLOADED_DATA_ALLOW = ['csv', 'json']

    # docs
    API_DOC_MEMBER = ['api']
    
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