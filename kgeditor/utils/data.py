import json
import logging
from kgeditor import redis_store
from kgeditor.constants import REDIS_CACHE_EXPIRES
def text2json(text):
    return json.loads(text)

def save_cache(set_key, data_key, data):
    data = json.dumps(data)
    try:
        pipeline = redis_store.pipeline()
        pipeline.multi()
        pipeline.hset(set_key, data_key, data)
        pipeline.expire(set_key, REDIS_CACHE_EXPIRES)
        pipeline.execute()
    except Exception as e:
        logging.error(e)

def get_cache(set_key, data_key):
    try:
        data = redis_store.hget(set_key, data_key)
    except Exception as e:
        logging.error(e)
    else:
        return data

def del_cache(set_key):
    try:
        keys = redis_store.hkeys(set_key)
        logging.info(keys)
        num = redis_store.hdel(set_key, *keys)
        logging.info(num)
    except Exception as e:
        logging.error(e)