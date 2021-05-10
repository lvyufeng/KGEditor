from celery import Celery
from config import CeleryConfig

celery_app = Celery('tasks')
celery_app.config_from_object(CeleryConfig)

celery_app.autodiscover_tasks(
    [
        "tasks.import_triple_data",
        "tasks.import_raw_data",
        "tasks.graph_merge_task",
        "annotation_task"
    ]
)
