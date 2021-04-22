from celery import Celery
from config import CeleryConfig

celery_app = Celery('tasks')
celery_app.config_from_object(CeleryConfig)

celery_app.autodiscover_tasks()
