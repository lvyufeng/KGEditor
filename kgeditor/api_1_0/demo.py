from . import api
from flask import current_app
import logging
from kgeditor import db, models

@api.route("/demo")
def index():
    logging.debug('info msg')
    logging.info('info msg')
    logging.warn('info msg')
    return "index"